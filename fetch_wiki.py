"""한국어 위키백과 날짜별 피드에서 필요한 항목만 골라 today.json으로 저장합니다. 외부 패키지 불필요."""

import argparse
from datetime import datetime, timedelta
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")
FEED_URL = "https://api.wikimedia.org/feed/v1/wikipedia/ko/featured/{:%Y/%m/%d}"
# Wikimedia API는 연락 가능한 User-Agent를 요구합니다.
USER_AGENT = "daily-quote-project/1.0 (https://github.com/hgehgehge-art/daily-quote-project)"
MOSTREAD_LIMIT = 10


def fetch_feed(target_date):
    request = Request(FEED_URL.format(target_date), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def strip_html(text):
    """news의 story는 HTML이므로 태그를 지우고 공백을 정리합니다."""
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", text or ""))).strip()


def page_url(item):
    return item.get("content_urls", {}).get("desktop", {}).get("page", "")


def summarize(feed, mostread_feed):
    mostread = mostread_feed.get("mostread", {})
    image = feed.get("image", {})
    return {
        "mostread_date": mostread.get("date", "").rstrip("Z"),
        "mostread": [
            {"rank": number, "title": article.get("normalizedtitle") or article.get("title", ""),
             "description": article.get("description", ""), "views": article.get("views", 0),
             "url": page_url(article)}
            for number, article in enumerate(mostread.get("articles", [])[:MOSTREAD_LIMIT], 1)
        ],
        "image": {
            "title": image.get("title", ""),
            "description": strip_html(image.get("description", {}).get("text", "")),
            "artist": strip_html(image.get("artist", {}).get("text", "")),
            "license": image.get("license", {}).get("type", ""),
            "file_page": image.get("file_page", ""),
            "thumbnail": image.get("thumbnail", {}).get("source", ""),
        } if image else None,
        "news": [strip_html(item.get("story", "")) for item in feed.get("news", [])],
    }


def atomic_write(output, content):
    """같은 폴더에 임시 파일을 완성한 뒤 교체하여 기존 JSON의 손상을 막습니다."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent,
                                         prefix=f".{output.name}.", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="한국어 위키백과 오늘의 데이터를 JSON으로 저장합니다.")
    parser.add_argument("--output", default="today.json", type=Path, help="출력 JSON 경로")
    args = parser.parse_args(argv)
    try:
        fetched_at = datetime.now(KST)
        target_date = fetched_at.date()
        feed = fetch_feed(target_date)
        # 조회수 집계는 UTC 하루가 끝나야 나오므로, 한국 자정 직후에는 전날 피드에서 가져옵니다.
        mostread_feed = feed if "mostread" in feed else fetch_feed(target_date - timedelta(days=1))
        data = {
            "date": target_date.isoformat(),
            "fetched_at": fetched_at.isoformat(timespec="seconds"),
            "source": FEED_URL.format(target_date),
            "attribution": "위키백과(ko.wikipedia.org) · 텍스트 CC BY-SA 4.0 · 사진은 image.license 참고",
            **summarize(feed, mostread_feed),
        }
        if not data["mostread"] and data["image"] is None and not data["news"]:
            raise ValueError("피드에 저장할 항목이 없습니다.")
        atomic_write(args.output, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    except (HTTPError, URLError, OSError, ValueError) as error:
        print(f"가져오기 실패: {error}", file=sys.stderr)
        return 1
    print(f"날짜 {data['date']} · 많이 본 문서 {len(data['mostread'])}개({data['mostread_date']}) · "
          f"뉴스 {len(data['news'])}개 · 사진 {'있음' if data['image'] else '없음'}")
    print(f"JSON 저장 완료: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

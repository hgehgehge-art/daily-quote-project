# 오늘의 한 문장

**문구 목록에서 한국 날짜에 맞는 항목을 고르고, 웹페이지를 만들어 GitHub Pages에 배포하는 예제**입니다. Hello Actions에서 확인한 ‘명령 실행’을 ‘웹 생성과 배포’로 확장합니다. Python 표준 라이브러리를 사용하며 외부 뉴스, RSS, API 키가 필요하지 않습니다.

```text
main에 저장 / 버튼으로 실행 / 예약 시각 도달
  → GitHub Actions가 Python 실행
  → quotes.json에서 날짜에 맞는 문구 선택
  → _site/index.html 생성
  → GitHub Pages에 직접 배포
```

## 파일 역할

| 파일 | 역할 |
|---|---|
| `quotes.json` | 문구·작성 표시·주제의 목록. 학생이 바꿀 데이터 |
| `main.py` | 한국 날짜 선택, 문구 선택, HTML 생성 |
| `index.html` | 복사 직후 열어 볼 수 있는 생성된 웹 저장본 |
| `.github/workflows/daily_quote.yml` | 실행 조건, Python 실행, Pages 배포 |
| `문구이용안내.md` | 제공 문구의 복제·수정·공개·배포 안내 |

생성 결과는 정적 HTML입니다. 웹페이지를 새로고침해도 Python은 실행되지 않습니다. **Actions가 다시 생성하고 배포해야** 공개 웹의 문구와 생성 시각이 갱신됩니다. Actions가 끝나면 실행용 컴퓨터도 작업을 마칩니다.

## 1. 예제 파일 복사

압축을 풀고 **`daily-quote-project` 폴더의 내용 전체**를 새 저장소의 최상위에 넣습니다. 최상위가 다음 구조인지 확인하세요.

```text
daily-quote-project/          ← 이 폴더를 작업 폴더로 열기
├── main.py
├── quotes.json
├── index.html
├── README.md
├── 문구이용안내.md
├── .gitignore
└── .github/
    └── workflows/
        └── daily_quote.yml
```

`workflows/daily_quote.yml`만 있거나, 저장소 안에 다시 `daily-quote-project/.github/...`로 중첩되면 인식되지 않습니다. **저장소 루트의 `.github/workflows/daily_quote.yml`**이어야 합니다. macOS Finder에서는 `Command + Shift + .`으로 숨김 폴더를 표시할 수 있습니다. GitHub 웹에서 파일을 직접 만들 때는 파일 이름에 `.github/workflows/daily_quote.yml` 전체 경로를 입력하세요.

이번 예제는 별도 Public 저장소 `daily-quote-project`에 배포하는 것을 권장합니다. 기존 개인 홈페이지 저장소를 사용하면 그 사이트가 이 예제로 바뀔 수 있습니다. 기존 `hello.yml`을 함께 둘 수 있지만, 다른 Pages 배포 워크플로가 동시에 같은 사이트를 배포하지 않도록 확인하세요.

### 브라우저로 파일을 올릴 때

1. GitHub의 **New repository**에서 Public·README 초기화로 새 저장소를 만듭니다. 실제 기본 브랜치가 `main`인지 확인합니다.
2. 저장소 첫 화면의 **Add file → Upload files**에서 `main.py`, `quotes.json`, `index.html`, `README.md`, `문구이용안내.md`를 올립니다. 폴더째나 ZIP째 올리지 않고 **안의 파일**을 루트에 저장합니다. `.gitignore`는 함께 올리면 좋지만 실행 필수 파일은 아닙니다.
3. 숨김 `.github` 업로드가 빠지지 않도록 **Code 첫 화면 → Add file → Create new file**을 누르고 이름에 **`.github/workflows/daily_quote.yml`** 전체 경로를 입력합니다.
4. 제공 워크플로 파일을 텍스트 편집기로 열어 전체 내용을 복사합니다. GitHub 편집창에는 코드만 붙여 넣고 main에 **Commit changes**합니다.
5. 저장 후 경로가 **저장소 / .github / workflows / daily_quote.yml**인지 확인하고 아래 3단계의 Pages 설정·수동 실행으로 이어갑니다.

## 2. 로컬에서 먼저 확인하기 — 선택

복사한 `index.html`을 브라우저로 열면 제공된 저장본이 보입니다. 오늘 날짜로 새로 만들려면 Python 3.9 이상이 있는 macOS 또는 Linux에서 프로젝트 폴더를 열고 실행하세요. GitHub 실습에서는 로컬 Python 설치 없이 Actions로 바로 실행해도 됩니다.

```bash
python3 main.py
```

생성된 `index.html`을 다시 열거나 새로고침합니다. 페이지 하단의 ‘마지막 생성’은 실제 실행 시각이며 한국시간(KST)입니다. 로컬 실행 결과에는 ‘로컬 생성본’이 표시됩니다.

다른 날짜의 결과를 확인할 때는 별도 출력 파일을 사용하세요.

```bash
python3 main.py --date 2026-09-23 --output preview.html
```

`preview.html`에는 **‘날짜 미리보기’**가 표시됩니다. 미리보기 날짜가 실제 오늘과 같아도 이 표시는 유지됩니다. 화면의 ‘선택한 날짜의 전날’은 미리보기 날짜 바로 전날입니다. 이 기능은 시간 여행이나 실제 예약 실행 기록이 아닙니다.

## 3. GitHub Pages에 배포하기

1. Public 저장소 `daily-quote-project`를 만들고, 위 파일을 `main` 브랜치 최상위에 저장합니다.
2. **Settings → Pages → Build and deployment → Source → GitHub Actions**를 선택합니다. 제공된 워크플로를 사용하므로 추천 Jekyll·Static HTML 템플릿을 추가하지 않습니다.
3. **Actions → Daily Quote Generator → Run workflow**를 엽니다.
4. 브랜치는 `main`, **`preview_date`는 비워 둔 상태**로 Run workflow를 누릅니다.
5. 실행 항목을 열어 **`build`와 `deploy`가 모두 초록색**인지 확인합니다. `build`의 `Generate daily page` 로그에는 선택 날짜와 생성 시각이 표시됩니다.
6. 실행 결과의 배포 링크 또는 Settings → Pages에 표시된 **실제 공개 URL**을 엽니다.

일반 프로젝트 저장소의 주소 형태는 `https://아이디.github.io/daily-quote-project/`입니다. `아이디.github.io`라는 이름의 개인 홈페이지 저장소만 루트 주소를 사용합니다. 추측한 주소 대신 **배포 결과의 실제 링크**를 사용하세요.

첫 Push 때 Pages 설정이 아직 안 되어 있으면 실행이 실패할 수 있습니다. Source 설정을 마친 뒤 수동으로 다시 실행하세요. 액션 실행이 조직 정책으로 제한된 계정은 해당 안내에 따라 허용 여부를 확인해야 합니다.

**저장소의 `index.html`이 매번 커밋되는 방식이 아닙니다.** Actions는 `_site/index.html`을 생성한 뒤 배포 파일 묶음(artifact)으로 전달합니다. 결과는 Code 탭의 저장본이 아니라 **공개 웹과 Actions 로그**에서 확인합니다. 별도 토큰이나 `contents: write` 권한이 필요하지 않습니다.

## 4. 수업 중 갱신을 확인하는 방법

| 실험 | 예상 결과 | 확인할 증거 |
|---|---|---|
| 같은 날, 입력 없이 다시 실행 | 같은 문구 유지 | 마지막 생성 시각·Actions 실행번호 변화 |
| `preview_date`에 오늘 다음 날 입력 | 다음 날짜의 문구 표시 | 선택 날짜·‘날짜 미리보기’ 배지·문구 |
| `quotes.json`의 현재 문구 수정 후 Commit | 수정된 문구로 생성·배포 | 수정한 문구·커밋 번호·Actions 성공 |
| `preview_date`를 비워 다시 실행 | 실제 한국 날짜 화면으로 복귀 | ‘한국 날짜 기준’ 표시 |

**수동 날짜 미리보기도 공개 사이트에 배포됩니다.** 실험을 마치면 입력을 비워 재실행해 오늘 날짜로 되돌리세요. 같은 실행을 `Re-run jobs`로 재시도하면 실행번호는 같고 시도 번호가 달라질 수 있습니다.

문구 선택은 `(날짜 순번 - 1) % 문구 개수`입니다. 같은 날짜·같은 순서의 목록에서는 같은 항목이 선택되고, 다음 날에는 다음 항목으로 이동합니다. 제공된 서로 다른 16개 문구는 16일마다 반복됩니다. 목록의 순서나 개수가 바뀌면 같은 날짜에도 선택되는 항목이 달라질 수 있습니다.

## 5. 매일 예약 실행하기

기본 배포본은 예약 실행이 꺼져 있습니다. 수동 배포에 성공한 뒤 `.github/workflows/daily_quote.yml`의 예약 두 줄에서 **`#`과 그 바로 뒤 공백 한 칸을 제거**하고 `main`에 저장하세요. `schedule`은 `push`, `workflow_dispatch`와 같은 들여쓰기 수준입니다. 아래 모양과 같으면 됩니다.

```yaml
  schedule:
    - cron: '17 23 * * *'  # UTC 23:17 = 다음 날 한국시간 08:17, 매일
```

예약은 기본 브랜치의 워크플로를 사용합니다. 이 실습에서는 기본 브랜치를 `main`으로 둡니다. 예약 시각은 UTC 기준이며, 생성할 문구의 날짜는 코드에서 한국시간으로 계산합니다.

예약 시각은 정확한 실행 시작을 보장하지 않으며 지연될 수 있습니다. 공개 저장소에서 장기간 활동이 없으면 예약이 비활성화될 수 있습니다. **수업에서는 예약 설정을 확인하고, 다음 날에는 Event가 `schedule`인 실행 기록과 공개 웹의 생성 시각을 확인**하세요. 수동 실행 성공은 예약 실행 성공의 증거가 아닙니다. [GitHub 예약 실행 안내](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## 6. 문구 바꾸기와 팀 활동

`quotes.json`은 아래 객체들의 배열입니다. 쉼표·큰따옴표를 유지하고, 마지막 항목 뒤에는 쉼표를 붙이지 마세요.

```json
[
  {"quote": "오늘 이해한 한 줄을 내일의 내가 읽을 수 있게 남겨 두자.", "author": "수업 예제", "topic": "기록"},
  {"quote": "막힌 지점을 설명하다 보면 다음에 해 볼 일이 보인다.", "author": "수업 예제", "topic": "문제 해결"}
]
```

제공 문구의 이용 범위는 [문구 이용 안내](문구이용안내.md)를 읽으세요. 추가한 콘텐츠는 직접 작성하거나 공개 사용 조건을 확인합니다.

3인 팀의 공통 미션은 **‘팀이 정한 사용자에게 필요한 정보를 자동으로 갱신해 보여 주는 웹서비스 만들기’**입니다. 데이터와 주제는 자유롭게 정합니다. 오늘의 질문·학습 팁·미니 퀴즈·팀 미션은 선택 가능한 아이디어이며 필수 주제가 아닙니다. 역할을 나누되 전원이 실행 조건, 데이터 처리, 배포 결과를 설명할 수 있어야 합니다.

## 7. Codex 또는 Claude Code에 요청할 때

Codex 앱에서는 이 폴더를 로컬 프로젝트에 연결합니다. CLI를 쓰면 터미널에서 이 폴더로 이동한 뒤 `codex` 또는 `claude`를 실행합니다. 두 도구를 함께 쓸 필요는 없습니다. 도구 이용 가능 여부와 사용 한도는 각 계정·요금제에 따릅니다.

Git·GitHub CLI(`gh`) 설치·로그인 상태를 확인하고 계정 인증은 본인이 진행합니다. 다음 요청은 공개 저장소 생성·배포와 수동 성공 후 예약 활성화를 포함합니다. 도구가 못 한 단계는 GitHub 화면에서 직접 이어갑니다.

```text
현재 폴더의 ‘오늘의 한 문장’ 예제를 GitHub Actions와 Pages로 배포해줘.

1. README, main.py, quotes.json, .github/workflows/daily_quote.yml을 읽고
   현재 폴더·Git 상태·브랜치·원격 저장소를 먼저 확인해줘.
   예제 폴더를 한 겹 더 넣지 말고 코드가 저장소 최상위에 오게 해줘.
2. Git과 GitHub CLI 설치·로그인 상태를 확인해줘.
   설치나 인증이 필요하면 내가 직접 진행할 수 있게 안내해줘.
3. 내 계정에 daily-quote-project라는 Public 저장소를 만들고 main에 올려줘.
   같은 이름의 저장소가 있거나 기존 홈페이지를 바꾸게 되면 덮어쓰지 말고 알려줘.
   실습안내·활동기록·인증 파일은 올리지 말고 예제 코드만 커밋·Push해줘.
4. Pages Source를 GitHub Actions로 설정해줘. 기존 배포 워크플로를 사용하고
   별도의 Jekyll·Static HTML 배포 템플릿을 추가하지 마.
5. Daily Quote Generator를 main에서 preview_date를 비워 실행해줘.
   build와 deploy의 실제 로그를 확인하고, 실패하면 원인을 수정해줘.
6. 공개 웹의 한국 날짜·문구·실제 생성 시각을 확인해줘.
   같은 날짜·같은 문구 목록이면 같은 문장이 나오는 것은 정상이야.
7. 수동 배포가 성공하면 daily_quote.yml의 예약 주석 두 줄을 활성화하고
   main에 커밋·Push해줘. cron은 17 23 * * *로 유지해줘.
   이 수정 커밋의 build·deploy 성공도 확인해줘.
   한국시간 매일 08:17 예약 설정과 실제 예약 실행 관찰을 구분해줘.
8. 공개 URL·Actions 실행 URL·배포 커밋과 확인한 결과를 알려줘.
   도구나 권한 때문에 못 한 단계는 미완료로 적고, 내가 따라 할 수동 순서를 알려줘.

외부 API·API 키는 추가하지 마. 날짜 미리보기로 테스트했다면
preview_date를 비워 다시 실행해 실제 오늘 날짜로 복원해줘.
```

[공식 OpenAI Codex CLI 안내](https://learn.chatgpt.com/docs/codex/cli), [Claude Code 시작 안내](https://code.claude.com/docs/en/quickstart)

## 자주 막히는 지점

| 증상 | 확인할 것 |
|---|---|
| Daily Quote Generator가 안 보임 | `main`에 `.github/workflows/daily_quote.yml`로 저장했는지 |
| Configure Pages에서 실패 | Settings → Pages → Source가 GitHub Actions인지 |
| Generate daily page에서 실패 | JSON 문법·빈 목록·날짜 형식. 로그의 오류 문장 확인 |
| 문구가 그대로임 | 같은 날짜·같은 목록이면 정상. 생성 시각과 실행번호도 비교 |
| 공개 웹이 예전 화면임 | 최신 `deploy` 성공 여부와 실제 배포 URL, 브라우저 새로고침 확인 |
| 미래 날짜가 표시됨 | `preview_date`를 비워 다시 실행 |
| 예약 기록이 아직 없음 | 기본 브랜치에 예약 저장, UTC 환산, 실제 예약 시각 경과 여부 확인 |

빈 목록·잘못된 JSON·잘못된 날짜가 들어오면 새 HTML 생성을 중단합니다. 실패한 빌드는 배포하지 않으므로 이전에 배포된 웹은 그대로 남습니다.

## 공식 참고 자료

- [GitHub Pages 배포 소스 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [사용자 지정 Actions로 Pages 배포](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [워크플로 수동 실행](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [공식 Pages artifact Action](https://github.com/actions/upload-pages-artifact)

워크플로의 Action 버전과 공식 안내 확인: 2026-09-22. 이 파일은 실습용 안내이며, 학생 계정의 실제 배포 성공은 각자의 실행 로그와 공개 URL에서 확인합니다.

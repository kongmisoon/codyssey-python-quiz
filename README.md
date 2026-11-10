# 🎯 나만의 퀴즈 게임

터미널에서 동작하는 Python 콘솔 퀴즈 게임입니다. 퀴즈 풀기·추가·목록·최고 점수 확인 기능을 제공하며,
`state.json`에 데이터를 저장해서 프로그램을 종료했다 다시 실행해도 퀴즈와 최고 점수가 유지됩니다.

## 1. 프로젝트 개요

- 언어/환경: Python 3.10 이상, 외부 라이브러리 없음 (표준 라이브러리 `json`, `os`만 사용)
- 구조: `Quiz`(문제 1개) / `QuizGame`(게임 전체) 두 클래스로 역할 분리
- 안정성: 잘못된 입력, `Ctrl+C`, 입력 스트림 종료(EOF), 데이터 파일 없음·손상 상황에서도 비정상 종료되지 않음
- Git: 기능 단위 커밋, 브랜치(`feature/play-quiz`) 생성 및 병합, clone/pull 실습 기록 포함

## 2. 퀴즈 주제 선정 이유

주제는 **한국음식, 그중에서도 발효음식(김치·된장·고추장)과 K-food**입니다.

저는 한국음식을 사랑하고, 건강한 K-food를 세계에 알리고 싶다는 열정이 있습니다.
해외에서 살다 오면서 김치, 된장, 고추장 같은 발효음식이 건강에 과학적으로 이로운 음식이라는 점을
더 깊이 느꼈습니다. 앞으로는 한국음식을 아트와 연결해 예술로 승화시키는 것이 꿈이고,
이 프로젝트는 그 꿈을 향한 첫 포트폴리오 작업입니다.
퀴즈 게임이라는 형식이라면 한국음식의 재료, 발효 원리, 문화적 가치를 쉽고 재미있게 전달할 수 있고,
직접 퀴즈를 추가하면서 내용을 계속 키워 갈 수 있다고 생각해 이 주제를 선택했습니다.

## 3. 실행 방법

```bash
git clone <저장소 URL>
cd codyssey-python-quiz
python main.py        # 또는 python3 main.py
```

테스트 실행:

```bash
python -m unittest discover -s tests -v
```

## 4. 기능 목록

| 메뉴 | 기능 |
|---|---|
| 1. 퀴즈 풀기 | 저장된 퀴즈를 순서대로 출제, 정답/오답 안내, 결과(점수) 표시, 최고 점수 갱신. 퀴즈가 없으면 안내 |
| 2. 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 등록하고 즉시 파일에 저장 |
| 3. 퀴즈 목록 | 등록된 문제 목록 표시. 퀴즈가 없으면 안내 |
| 4. 점수 확인 | 최고 점수 표시. 아직 풀지 않았다면 안내 |
| 5. 종료 | 저장 후 종료 |

공통 입력 처리 (`input_utils.get_int_input`):

- 앞뒤 공백 제거
- 빈 입력, 숫자가 아닌 입력, 허용 범위 밖 숫자 → 안내 메시지 후 재입력
- `Ctrl+C` / EOF → 안내 메시지 출력, 저장 후 정상 종료

## 5. 파일 구조

```
codyssey-python-quiz/
├── main.py              # 진입점
├── quiz.py              # Quiz 클래스 (출력, 정답 확인, dict 변환)
├── quiz_game.py         # QuizGame 클래스 (메뉴, 기능, 저장/불러오기)
├── input_utils.py       # 공통 입력 검증 함수
├── default_quizzes.py   # 기본 퀴즈 6개 (Quiz 인스턴스로 생성)
├── tests/
│   └── test_quiz_game.py
├── docs/screenshots/    # 실행 화면 캡처 (menu / play / add_quiz / score)
├── state.json           # 실행 시 자동 생성되는 데이터 파일 (.gitignore 처리)
├── .gitignore
└── README.md
```

## 6. 데이터 파일 (`state.json`)

- 경로: 프로젝트 루트 `state.json` (UTF-8, `ensure_ascii=False`)
- 역할: 퀴즈 목록과 최고 점수를 저장해 프로그램 재실행 후에도 유지
- 생성: 첫 실행 시 파일이 없으면 기본 퀴즈로 시작하고, 퀴즈 추가·최고 점수 갱신·종료 시 저장
- 복구: 파일이 손상되었거나 형식이 맞지 않으면 안내 메시지를 출력하고 기본 퀴즈로 초기화
- 개인 진행 상황이 담기므로 Git 추적 대상에서 제외했습니다.

스키마:

```json
{
    "quizzes": [
        {
            "question": "김치, 된장처럼 미생물이 재료를 분해하고 변화시켜 새로운 맛과 영양을 만드는 과정은?",
            "choices": ["증류", "발효", "냉동", "건조"],
            "answer": 2
        }
    ],
    "best_score": 83,
    "best_correct": 5,
    "best_total": 6
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int \| null | 최고 점수(0~100). 아직 풀지 않았다면 `null` |
| `best_correct` / `best_total` | int | 최고 점수 때의 정답 수 / 전체 문제 수 |

점수는 `정답 수 / 전체 문제 수 × 100`을 반올림한 값입니다.

## 7. 실행 화면

| 메뉴 | 퀴즈 풀기 | 퀴즈 추가 | 점수 확인 |
|---|---|---|---|
| `docs/screenshots/menu.png` | `docs/screenshots/play.png` | `docs/screenshots/add_quiz.png` | `docs/screenshots/score.png` |

## 8. Git 작업 방식

- 커밋 메시지: `Feat:` / `Fix:` / `Docs:` / `Refactor:` / `Test:` 접두어 + 작업 내용
- 퀴즈 풀기는 `feature/play-quiz` 브랜치에서 작업한 뒤 `main`에 병합
- clone/pull 실습: 저장소를 clone한 복제본에서 README를 수정해 push한 뒤, 원본 폴더에서 pull로 받아 반영했습니다. (커밋 `62bdd40`)

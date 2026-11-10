"""기본 퀴즈 데이터 (주제: Python & Git 기초)."""

from quiz import Quiz


def get_default_quizzes():
    """첫 실행 또는 데이터 파일 손상 시 사용하는 기본 퀴즈 목록을 만들어 반환한다."""
    return [
        Quiz(
            "순서가 있고 값을 수정할 수 있는 Python 자료형은?",
            ["int", "tuple", "list", "str"],
            3,
        ),
        Quiz(
            "객체가 만들어질 때 자동으로 호출되어 속성을 초기화하는 메서드는?",
            ["__init__", "__str__", "__call__", "__repr__"],
            1,
        ),
        Quiz(
            "변경사항을 커밋 대상(staging)에 올리는 Git 명령어는?",
            ["git commit", "git push", "git clone", "git add"],
            4,
        ),
        Quiz(
            "원격 저장소를 내 컴퓨터에 통째로 복제하는 Git 명령어는?",
            ["git pull", "git clone", "git init", "git merge"],
            2,
        ),
        Quiz(
            "프로그램을 종료해도 데이터가 사라지지 않고 남아 있는 성질을 뜻하는 용어는?",
            ["캡슐화", "재귀", "데이터 영속성", "다형성"],
            3,
        ),
        Quiz(
            "한글이 \\uXXXX로 깨지지 않게 json.dump로 저장할 때 지정하는 옵션은?",
            ["indent=4", "sort_keys=True", "default=str", "ensure_ascii=False"],
            4,
        ),
    ]

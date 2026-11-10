"""공통 입력 처리 함수 모음.

모든 숫자/문자 입력은 이 모듈의 함수를 거치도록 해서
검증 로직이 한 곳에만 존재하도록 한다.

KeyboardInterrupt(Ctrl+C), EOFError(입력 스트림 종료)는 여기서 잡지 않고
호출한 쪽(QuizGame.run)에서 한 번에 처리한다.
"""


def get_int_input(prompt, min_value, max_value):
    """min_value ~ max_value 범위의 정수를 입력받아 반환한다.

    - 앞뒤 공백은 제거한다.
    - 빈 입력, 숫자가 아닌 입력, 범위 밖 숫자는 안내 후 다시 입력받는다.
    """
    while True:
        raw = input(prompt).strip()

        if not raw:
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if not min_value <= number <= max_value:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


def get_text_input(prompt):
    """공백만 있는 입력을 허용하지 않는 문자열 입력 함수."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

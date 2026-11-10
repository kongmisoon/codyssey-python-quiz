"""Quiz 클래스: 퀴즈 한 문제를 표현한다."""


class Quiz:
    CHOICE_COUNT = 4  # 선택지 개수 (정답 번호는 1 ~ CHOICE_COUNT)

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if (
            not isinstance(answer, int)
            or isinstance(answer, bool)
            or not 1 <= answer <= self.CHOICE_COUNT
        ):
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이의 정수여야 합니다.")

        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer  # 1부터 시작하는 번호

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장용 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """dict(JSON에서 읽은 값)로부터 Quiz 객체를 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 객체(dict)여야 합니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except KeyError as error:
            raise ValueError(f"퀴즈 데이터에 {error} 항목이 없습니다.") from error

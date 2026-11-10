"""QuizGame 클래스: 게임 전체(메뉴, 흐름, 저장)를 관리한다."""

from default_quizzes import get_default_quizzes
from input_utils import get_int_input, get_text_input
from quiz import Quiz


class QuizGame:
    LINE_WIDTH = 40
    MENU_ITEMS = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")
    EXIT_CHOICE = len(MENU_ITEMS)

    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None  # None이면 아직 퀴즈를 푼 적이 없음
        self.best_correct = 0
        self.best_total = 0

    # ---------- 출력 헬퍼 ----------
    def print_line(self, char="-"):
        print(char * self.LINE_WIDTH)

    # ---------- 메뉴 ----------
    def show_menu(self):
        print()
        self.print_line("=")
        print("        🎯 나만의 퀴즈 게임 🎯")
        self.print_line("=")
        for number, title in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {title}")
        self.print_line("=")

    def handle_choice(self, choice):
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.show_quizzes,
            4: self.show_best_score,
        }
        actions[choice]()

    def run(self):
        """메인 루프. 종료 번호를 선택하면 끝난다."""
        while True:
            self.show_menu()
            choice = get_int_input("선택: ", 1, self.EXIT_CHOICE)
            if choice == self.EXIT_CHOICE:
                print("👋 게임을 종료합니다. 안녕히 가세요!")
                break
            self.handle_choice(choice)

    # ---------- 퀴즈 풀기 ----------
    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_question(number, quiz):
                correct += 1

        self.show_result(correct, total)

    def ask_question(self, number, quiz):
        """한 문제를 출제하고 정답이면 True를 반환한다."""
        print()
        self.print_line("-")
        quiz.display(number)
        user_answer = get_int_input("\n정답 입력: ", 1, Quiz.CHOICE_COUNT)

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            return True
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]})입니다.")
        return False

    def show_result(self, correct, total):
        """결과를 출력하고 최고 점수를 갱신한다."""
        score = round(correct / total * 100)
        print()
        self.print_line("=")
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(score, correct, total):
            print("🎉 새로운 최고 점수입니다!")
        self.print_line("=")

    def update_best_score(self, score, correct, total):
        """최고 점수보다 높으면 갱신하고 True를 반환한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            return True
        return False

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = get_text_input("문제를 입력하세요: ")
        choices = [
            get_text_input(f"선택지 {number}: ")
            for number in range(1, Quiz.CHOICE_COUNT + 1)
        ]
        answer = get_int_input(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!")

    # ---------- 퀴즈 목록 ----------
    def show_quizzes(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. '퀴즈 추가'로 만들어 보세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        self.print_line("-")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        self.print_line("-")

    # ---------- 점수 확인 ----------
    def show_best_score(self):
        """최고 점수를 출력한다. 아직 풀지 않았다면 안내 메시지를 보여 준다."""
        if self.best_score is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. '퀴즈 풀기'에 도전해 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct}문제 정답)")

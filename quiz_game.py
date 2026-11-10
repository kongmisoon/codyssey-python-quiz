"""QuizGame 클래스: 게임 전체(메뉴, 흐름, 저장)를 관리한다."""

from default_quizzes import get_default_quizzes
from input_utils import get_int_input
from quiz import Quiz


class QuizGame:
    MENU_WIDTH = 40

    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None

    # ---------- 메뉴 ----------
    def show_menu(self):
        print()
        print("=" * self.MENU_WIDTH)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * self.MENU_WIDTH)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * self.MENU_WIDTH)

    def handle_choice(self, choice):
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.show_quizzes,
            4: self.show_best_score,
        }
        actions[choice]()

    def run(self):
        """메인 루프. 5번(종료)을 선택하면 끝난다."""
        while True:
            self.show_menu()
            choice = get_int_input("선택: ", 1, 5)
            if choice == 5:
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
            print("\n" + "-" * 40)
            quiz.display(number)
            user_answer = get_int_input("\n정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]})입니다.")

        score = round(correct / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)

    # ---------- 아직 구현되지 않은 기능 (이후 커밋에서 채움) ----------

    def add_quiz(self):
        print("🚧 준비 중입니다.")

    def show_quizzes(self):
        print("🚧 준비 중입니다.")

    def show_best_score(self):
        print("🚧 준비 중입니다.")

"""QuizGame 클래스: 게임 전체(메뉴, 흐름, 저장)를 관리한다."""

from input_utils import get_int_input


class QuizGame:
    MENU_WIDTH = 40

    def __init__(self):
        self.quizzes = []
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

    # ---------- 아직 구현되지 않은 기능 (이후 커밋에서 채움) ----------
    def play_quiz(self):
        print("🚧 준비 중입니다.")

    def add_quiz(self):
        print("🚧 준비 중입니다.")

    def show_quizzes(self):
        print("🚧 준비 중입니다.")

    def show_best_score(self):
        print("🚧 준비 중입니다.")

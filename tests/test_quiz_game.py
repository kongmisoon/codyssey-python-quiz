"""퀴즈 게임 단위 테스트. 실행: python -m unittest discover -s tests -v"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from default_quizzes import get_default_quizzes  # noqa: E402
from input_utils import get_int_input  # noqa: E402
from quiz import Quiz  # noqa: E402
from quiz_game import QuizGame  # noqa: E402


def run_silently(func, *args, inputs=None):
    """input()을 inputs 목록으로 대체하고 출력을 캡처해서 (반환값, 출력문자열)을 돌려준다."""
    buffer = io.StringIO()
    patcher = mock.patch("builtins.input", side_effect=inputs) if inputs is not None else contextlib.nullcontext()
    with patcher, contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class QuizTest(unittest.TestCase):
    def test_correct_and_wrong_answer(self):
        quiz = Quiz("Q", ["a", "b", "c", "d"], 2)
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(3))

    def test_dict_round_trip(self):
        quiz = Quiz("한글 문제?", ["가", "나", "다", "라"], 4)
        self.assertEqual(Quiz.from_dict(quiz.to_dict()).to_dict(), quiz.to_dict())

    def test_invalid_data_raises_value_error(self):
        bad = [
            ("", ["a", "b", "c", "d"], 1),
            ("Q", ["a", "b", "c"], 1),
            ("Q", ["a", "b", "c", " "], 1),
            ("Q", ["a", "b", "c", "d"], 0),
            ("Q", ["a", "b", "c", "d"], 5),
            ("Q", ["a", "b", "c", "d"], True),
        ]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                Quiz(*args)

    def test_default_quizzes_at_least_five(self):
        self.assertGreaterEqual(len(get_default_quizzes()), 5)


class InputTest(unittest.TestCase):
    def test_retries_until_valid(self):
        # 빈 입력 → 문자 → 범위 밖(9, 0) → 공백 포함 정상 입력
        result, output = run_silently(get_int_input, "> ", 1, 5, inputs=["", "abc", "9", "0", "  3  "])
        self.assertEqual(result, 3)
        self.assertEqual(output.count("⚠️"), 4)

    def test_eof_and_interrupt_propagate(self):
        for error in (EOFError, KeyboardInterrupt):
            with self.subTest(error=error), self.assertRaises(error):
                run_silently(get_int_input, "> ", 1, 5, inputs=error)


class QuizGameTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "state.json")
        self.game = QuizGame(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def answers(self):
        return [str(q.answer) for q in self.game.quizzes]

    def test_first_run_uses_default_quizzes(self):
        _, output = run_silently(self.game.load_state)
        self.assertEqual(len(self.game.quizzes), len(get_default_quizzes()))
        self.assertIn("기본 퀴즈", output)

    def test_corrupted_file_is_recovered(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{broken json")
        _, output = run_silently(self.game.load_state)
        self.assertIn("손상", output)
        self.assertEqual(len(self.game.quizzes), len(get_default_quizzes()))
        with open(self.path, encoding="utf-8") as file:
            self.assertIn("quizzes", json.load(file))  # 복구된 파일은 정상 JSON

    def test_invalid_schema_is_treated_as_corrupted(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump({"quizzes": [{"question": "Q", "choices": ["a"], "answer": 1}]}, file)
        run_silently(self.game.load_state)
        self.assertEqual(len(self.game.quizzes), len(get_default_quizzes()))

    def test_save_and_load_keeps_quizzes_and_score(self):
        run_silently(
            self.game.add_quiz,
            inputs=["영화 '기생충'의 감독은?", "박찬욱", "봉준호", "김기덕", "이창동", "2"],
        )
        self.game.update_best_score(80, 4, 5)
        self.game.save_state()

        reloaded = QuizGame(self.path)
        run_silently(reloaded.load_state)
        self.assertEqual(len(reloaded.quizzes), len(get_default_quizzes()) + 1)
        self.assertEqual(reloaded.quizzes[-1].question, "영화 '기생충'의 감독은?")
        self.assertEqual((reloaded.best_score, reloaded.best_correct, reloaded.best_total), (80, 4, 5))
        with open(self.path, encoding="utf-8") as file:
            self.assertIn("기생충", file.read())  # 한글이 \u 이스케이프 없이 저장됨

    def test_play_all_correct_updates_best_score(self):
        _, output = run_silently(self.game.play_quiz, inputs=self.answers())
        self.assertEqual(self.game.best_score, 100)
        self.assertIn("새로운 최고 점수", output)

    def test_worse_score_does_not_replace_best(self):
        run_silently(self.game.play_quiz, inputs=self.answers())
        wrong = [str(q.answer % 4 + 1) for q in self.game.quizzes]
        _, output = run_silently(self.game.play_quiz, inputs=wrong)
        self.assertEqual(self.game.best_score, 100)
        self.assertNotIn("새로운 최고 점수", output)

    def test_empty_states(self):
        self.game.quizzes = []
        _, play = run_silently(self.game.play_quiz)
        _, listing = run_silently(self.game.show_quizzes)
        _, score = run_silently(self.game.show_best_score)
        self.assertIn("퀴즈가 없습니다", play)
        self.assertIn("퀴즈가 없습니다", listing)
        self.assertIn("아직 퀴즈를 풀지 않았습니다", score)

    def test_run_exits_safely_on_eof_and_interrupt_and_saves(self):
        for error in (EOFError, KeyboardInterrupt):
            with self.subTest(error=error):
                if os.path.exists(self.path):
                    os.remove(self.path)
                game = QuizGame(self.path)
                _, output = run_silently(game.run, inputs=error)  # 예외가 밖으로 나오면 실패
                self.assertIn("안전하게 종료", output)
                self.assertTrue(os.path.exists(self.path))

    def test_menu_rejects_invalid_then_exits(self):
        _, output = run_silently(self.game.run, inputs=["abc", "9", "", " 5 "])
        self.assertEqual(output.count("⚠️"), 3)
        self.assertIn("게임을 종료합니다", output)


if __name__ == "__main__":
    unittest.main()

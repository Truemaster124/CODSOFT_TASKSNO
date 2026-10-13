import contextlib
import io
import re
import unittest
from unittest.mock import patch

from task1_chatbot import chatbot
from task2_tictactoe import tictactoe as game
from task4_recommender import recommender as movies


class ChatbotTests(unittest.TestCase):
    def test_introduction_takes_priority_over_greeting(self):
        self.assertIn("Garv", chatbot.get_reply("Hi, my name is Garv"))

    def test_ai_does_not_match_airplane(self):
        self.assertIn(chatbot.get_reply("what is airplane"), chatbot.FALLBACKS)
        self.assertIn("machines", chatbot.get_reply("what is AI?"))

    def test_exit_requires_a_command(self):
        self.assertIsNotNone(re.search(chatbot.EXIT_PATTERN, "bye!"))
        self.assertIsNone(re.search(chatbot.EXIT_PATTERN, "do not quit yet"))


class GameTests(unittest.TestCase):
    def test_invalid_and_occupied_input(self):
        board = [game.HUMAN] + [game.EMPTY] * 8
        with patch("builtins.input", side_effect=["abc", "0", "10", "\u00b2", "1", "2"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(game.ask_human_move(board), 1)

    def test_computer_cannot_lose_from_either_start(self):
        def explore(board, human_turn):
            result = game.winner(board)
            self.assertNotEqual(result, game.HUMAN)
            if result or game.is_full(board):
                return
            if human_turn:
                for move in game.free_cells(board):
                    child = board.copy()
                    child[move] = game.HUMAN
                    explore(child, False)
            else:
                before = board.copy()
                move = game.best_move(board)
                self.assertEqual(board, before)
                self.assertIn(move, game.free_cells(board))
                child = board.copy()
                child[move] = game.AI
                explore(child, True)

        for human_first in (True, False):
            with self.subTest(human_first=human_first):
                explore([game.EMPTY] * 9, human_first)


class RecommendationTests(unittest.TestCase):
    def test_cosine_known_vectors_and_zero(self):
        self.assertAlmostEqual(movies.cosine({"a": 3, "b": 4}, {"a": 3}), 0.6)
        self.assertEqual(movies.cosine({}, {"a": 1}), 0)
        self.assertEqual(movies.cosine({"a": 0}, {"a": 2}), 0)

    def test_genre_results_exclude_input(self):
        results = movies.similar_movies("Titanic")
        self.assertAlmostEqual(results[0][0], 1.0)
        self.assertEqual(results[0][1], "The Notebook")
        self.assertNotIn("Titanic", [title for _, title in results])
        self.assertIsNone(movies.similar_movies("Unknown"))

    def test_predictions_exclude_rated_movies(self):
        for user in movies.RATINGS:
            predictions, neighbours = movies.recommend_for_user(user)
            self.assertNotIn(user, [name for _, name in neighbours])
            self.assertLessEqual(len(neighbours), 3)
            for score, title in predictions:
                self.assertNotIn(title, movies.RATINGS[user])
                self.assertTrue(1 <= score <= 5.000000001)
        self.assertIsNone(movies.recommend_for_user("Unknown"))


if __name__ == "__main__":
    unittest.main()

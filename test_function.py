import unittest
from project import Hangman
import sys
import time

# ANSI color codes for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

class TestHangman(unittest.TestCase):

    def setUp(self):
        """Set up a fresh game instance before each test."""
        self.game = Hangman()
        self.game.word = "PYTHON"  # Fixed word for testing
        self.game.correct_guesses = set()
        self.game.guessed_letters = set()
        self.game.lives = 5

    def print_test_info(self, message):
        """Helper function to print test info with a delay for better visualization."""
        sys.stdout.write(YELLOW + message + RESET + "\n")
        sys.stdout.flush()
        time.sleep(0.3)

    def test_initial_state(self):
        self.print_test_info("[TEST] Checking initial game state...")
        self.assertEqual(self.game.get_lives(), 5)
        self.assertFalse(self.game.has_won())
        self.assertEqual(self.game.display_word(), "_ _ _ _ _ _")
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)

    def test_correct_guess(self):
        self.print_test_info("[TEST] Making a correct guess (P)...")
        result = self.game.make_guess("P")
        self.assertEqual(result, "Good guess!")
        self.assertIn("P", self.game.correct_guesses)
        self.assertEqual(self.game.display_word(), "P _ _ _ _ _")
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)

    def test_wrong_guess(self):
        self.print_test_info("[TEST] Making a wrong guess (Z)...")
        result = self.game.make_guess("Z")
        self.assertEqual(result, "Wrong guess!")
        self.assertEqual(self.game.get_lives(), 4)
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)

    def test_repeated_guess(self):
        self.print_test_info("[TEST] Repeating a guess (P)...")
        self.game.make_guess("P")
        result = self.game.make_guess("P")
        self.assertEqual(result, "You already guessed that letter.")
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)

    def test_win_condition(self):
        self.print_test_info("[TEST] Guessing all correct letters (Winning the game)...")
        for letter in "PYTHON":
            self.game.make_guess(letter)
        self.assertTrue(self.game.has_won())
        self.assertEqual(self.game.make_guess("P"), "Congratulations! You've won!")
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)

    def test_lose_condition(self):
        self.print_test_info("[TEST] Making 5 wrong guesses (Losing the game)...")
        for letter in "ZXCVB":
            self.game.make_guess(letter)
        self.assertEqual(self.game.get_lives(), 0)
        self.assertEqual(self.game.make_guess("Q"), f"Game over! The word was {self.game.get_word()}.")
        print(GREEN + "[TEST COMPLETED SUCCESSFUL]" + RESET)


if __name__ == "__main__":
    print(BLUE + "\n========== Running Hangman Unit Tests ==========\n" + RESET)

    # Run tests and check for failures
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestHangman))

    if result.wasSuccessful():
        print(GREEN + "\n✅✅✅ ALL TESTS COMPLETED SUCCESSFULLY ✅✅✅" + RESET)
    else:
        print(RED + "\n❌❌❌ SOME TESTS FAILED ❌❌❌" + RESET)

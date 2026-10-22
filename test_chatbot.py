"""
================================================================================
UNIT TESTS FOR SMART AI CHATBOT
================================================================================
Automated test suite using Python's standard `unittest` framework to verify
intent matching, calculation accuracy, state management, and fallback responses.
================================================================================
"""

import datetime
import unittest
from chatbot import ChatState, process_response, safe_calculate, match_exit, get_current_date, get_current_time


class TestChatState(unittest.TestCase):
    """Tests for ChatState class."""

    def test_default_state(self):
        state = ChatState()
        self.assertEqual(state.user_name, "Friend")
        self.assertEqual(state.conversation_count, 0)
        self.assertTrue(state.is_active)

    def test_set_user_name(self):
        state = ChatState()
        state.set_user_name("  divya raj  ")
        self.assertEqual(state.user_name, "Divya Raj")

    def test_increment_conversation(self):
        state = ChatState()
        state.increment_conversation()
        state.increment_conversation()
        self.assertEqual(state.conversation_count, 2)


class TestArithmeticCalculator(unittest.TestCase):
    """Tests for safe_calculate function."""

    def test_addition(self):
        result = safe_calculate("calculate 25 + 75")
        self.assertIn("100", result)

    def test_multiplication(self):
        result = safe_calculate("what is 12 * 5")
        self.assertIn("60", result)

    def test_division(self):
        result = safe_calculate("compute 100 / 4")
        self.assertIn("25", result)

    def test_division_by_zero(self):
        result = safe_calculate("calculate 10 / 0")
        self.assertIn("Division by zero", result)

    def test_invalid_math_expression(self):
        result = safe_calculate("calculate abc + def")
        self.assertIn("basic numeric math operations", result)


class TestIntentHandlers(unittest.TestCase):
    """Tests for process_response intent matching."""

    def setUp(self):
        self.state = ChatState()
        self.state.set_user_name("Alice")

    def test_greeting_intent(self):
        response = process_response("hello there", self.state)
        self.assertIn("Alice", response)

    def test_how_are_you_intent(self):
        response = process_response("how are you?", self.state)
        self.assertIn("doing great", response)

    def test_thank_you_intent(self):
        response = process_response("thank you so much", self.state)
        self.assertIn("welcome", response.lower())

    def test_ai_definition_intent(self):
        response = process_response("what is AI?", self.state)
        self.assertIn("Artificial Intelligence", response)

    def test_machine_learning_intent(self):
        response = process_response("what is machine learning?", self.state)
        self.assertIn("Machine Learning", response)

    def test_python_creator_intent(self):
        response = process_response("who created python?", self.state)
        self.assertIn("Guido van Rossum", response)

    def test_date_intent(self):
        response = process_response("what is today's date?", self.state)
        self.assertIn("Today's date is", response)

    def test_time_intent(self):
        response = process_response("what time is it?", self.state)
        self.assertIn("current time is", response)

    def test_help_intent(self):
        response = process_response("help", self.state)
        self.assertIn("HELP MENU", response)

    def test_unknown_fallback_intent(self):
        response = process_response("xyz123 random unsupported query", self.state)
        self.assertTrue("didn't quite understand" in response or "outside my current knowledge" in response or "rule-based AI chatbot" in response)

    def test_exit_matcher(self):
        self.assertTrue(match_exit("bye"))
        self.assertTrue(match_exit("exit"))
        self.assertTrue(match_exit("quit"))
        self.assertFalse(match_exit("hello"))


if __name__ == "__main__":
    unittest.main()

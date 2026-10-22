"""
================================================================================
SMART AI CHATBOT - B.Tech AI Minor Project
================================================================================
Description: A rule-based AI chatbot implementing basic Natural Language Processing
             (NLP) concepts such as keyword extraction, regular expression pattern
             matching, and intent classification. Built purely with Python 3 standard libraries.

Author:      B.Tech AI Student
Language:    Python 3.8+
Libraries:   datetime, random, re, sys, math
================================================================================
"""

import datetime
import math
import random
import re
import sys

# ==============================================================================
# SESSION STATE CLASS
# ==============================================================================

class ChatState:
    """
    Class to maintain conversation state during the chatbot session.
    Tracks user details and conversation metrics.
    """
    def __init__(self):
        self.user_name = "Friend"
        self.conversation_count = 0
        self.is_active = True

    def set_user_name(self, name: str):
        """Sets and formats the user's name."""
        cleaned_name = name.strip().title()
        if cleaned_name:
            self.user_name = cleaned_name

    def increment_conversation(self):
        """Increments conversation counter."""
        self.conversation_count += 1


# ==============================================================================
# KNOWLEDGE BASE DATASETS
# ==============================================================================

# List of programming & AI jokes
JOKES = [
    "Why do programmers prefer dark mode?\n   Because light attracts bugs! 🐛",
    "There are 10 types of people in the world:\n   Those who understand binary, and those who don't! 😂",
    "Why did the AI go to therapy?\n   It had too many deep learning issues! 🤖🧠",
    "Why was the computer cold?\n   It left its Windows open! 🪟❄️",
    "How many programmers does it take to change a light bulb?\n   None. It's a hardware problem! 💡⚡",
    "Why do Python programmers prefer indentation over braces?\n   Because they like keeping things clean and readable! 🐍",
    "What is an algorithm?\n   A word used by programmers when they don't want to explain what they did! 🤫"
]

# List of interesting AI facts
AI_FACTS = [
    "The term 'Artificial Intelligence' was first coined by John McCarthy in 1956 at the Dartmouth Conference.",
    "Alan Turing proposed the 'Turing Test' in 1950 to measure whether a machine can exhibit human-like intelligence.",
    "In 1997, IBM's Deep Blue became the first computer chess system to defeat a reigning world chess champion, Garry Kasparov.",
    "Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language.",
    "Python is the most popular programming language for AI & Machine Learning due to its simplicity and rich ecosystem.",
    "Deep Learning neural networks are loosely inspired by the biological neural networks of the human brain.",
    "Rule-based chatbots rely on decision trees, pattern matching, and regex to generate deterministic responses."
]


# ==============================================================================
# HELPER FUNCTIONS & UTILITIES
# ==============================================================================

def get_current_date() -> str:
    """Returns formatted current date."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y")


def get_current_time() -> str:
    """Returns formatted current time."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M:%S %p")


def safe_calculate(expression: str) -> str:
    """
    Safely parses and evaluates basic arithmetic calculations (+, -, *, /, %, ^).
    Uses regex validation to prevent code execution security risks.

    Args:
        expression (str): Raw string containing arithmetic expression.

    Returns:
        str: Result message or error explanation.
    """
    try:
        # Check if the expression contains unsupported alphabetic characters (except 'calculate', 'compute', 'what', 'is', 'math')
        clean_words = re.sub(r'\b(calculate|compute|what|is|math|the|result|of|please|and|value|sum|product)\b', '', expression, flags=re.IGNORECASE).strip()

        if re.search(r'[a-zA-Z]', clean_words):
            return "I can only process basic numeric math operations (+, -, *, /, %, ^)."

        # Extract numerical and operator pattern (e.g. "calculate 25 * 4", "what is 10 + 5")
        clean_expr = re.sub(r'[^0-9\+\-\*\/\%\^\(\)\.\s]', '', clean_words).strip()
        
        # Replace '^' with '**' for exponentiation in Python evaluation
        clean_expr = clean_expr.replace('^', '**')

        if not clean_expr:
            return "Please provide a valid math expression (e.g., '12 + 5' or '100 / 4')."

        # Evaluate calculation safely with empty builtins dictionary for security
        result = eval(clean_expr, {"__builtins__": None}, {"math": math})
        
        # Format floating point results cleanly
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 4)

        return f"The result of ({clean_expr.replace('**', '^')}) is **{result}**."

    except ZeroDivisionError:
        return "Error: Division by zero is mathematically undefined!"
    except Exception:
        return "Sorry, I couldn't evaluate that math expression. Please format it clearly, e.g., 'calculate 15 * 4'."


def get_help_menu(user_name: str) -> str:
    """Returns structured help menu showing available chatbot capability topics."""
    return f"""
+======================================================================+
  SMART AI CHATBOT - HELP MENU FOR {user_name.upper()}
+======================================================================+
  Here are things you can ask me:

  1. GREETINGS & SMALL TALK:
     - "Hi", "Hello", "Hey"
     - "How are you?"
     - "Thank you"

  2. ARTIFICIAL INTELLIGENCE (AI):
     - "What is AI?" / "What is Artificial Intelligence?"
     - "What is Machine Learning?"
     - "What is Deep Learning?"
     - "What is NLP?"

  3. PYTHON PROGRAMMING:
     - "What is Python?"
     - "Who created Python?"
     - "Why is Python popular for AI?"
     - "What are Python data types?"

  4. UTILITIES & CALCULATIONS:
     - "What is the date?"
     - "What is the current time?"
     - "Calculate 25 * 4" or "What is 100 / 5?"

  5. FUN & ENTERTAINMENT:
     - "Tell me a joke"
     - "Share an AI fact"

  6. NAVIGATION:
     - "Help" (Displays this menu)
     - "Bye" or "Exit" (Ends conversation)
+======================================================================+"""


# ==============================================================================
# INTENT HANDLER FUNCTIONS (NLP RULE ENGINE)
# ==============================================================================

def match_exit(user_input: str) -> bool:
    """Checks if user wants to terminate session."""
    return bool(re.search(r'\b(bye|exit|quit|goodbye|stop|cya)\b', user_input, re.IGNORECASE))


def process_response(user_input: str, state: ChatState) -> str:
    """
    Central Intent Engine: Matches user input using regex patterns & keywords,
    then executes corresponding function to return personalized response.

    Args:
        user_input (str): Cleaned raw text input from user.
        state (ChatState): Current active conversation state instance.

    Returns:
        str: Response text generated by the rule engine.
    """
    text = user_input.strip().lower()
    name = state.user_name

    # --------------------------------------------------------------------------
    # 1. HELP MENU INTENT
    # --------------------------------------------------------------------------
    if re.search(r'\b(help|options|commands|what can you do|menu)\b', text):
        return get_help_menu(name)

    # --------------------------------------------------------------------------
    # 2. GREETINGS INTENT
    # --------------------------------------------------------------------------
    if re.search(r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening|wassup|sup)\b', text):
        greetings = [
            f"Hello {name}! How can I assist you today?",
            f"Hi {name}! Great to see you. What would you like to learn or calculate?",
            f"Hey {name}! Hope you are having a wonderful day. Ask me anything about AI or Python!"
        ]
        return random.choice(greetings)

    # --------------------------------------------------------------------------
    # 3. COURTESY / SMALL TALK INTENTS
    # --------------------------------------------------------------------------
    if re.search(r'\b(how are you|how are you doing|how do you do|how r u)\b', text):
        return (f"I'm doing great, thank you for asking, {name}! 🤖 "
                f"I am ready to help you with Python, AI, calculations, or fun facts. How are you?")

    if re.search(r'\b(thank you|thanks|thank u|thx|much appreciated)\b', text):
        responses = [
            f"You're very welcome, {name}! Happy to help.",
            f"Anytime, {name}! You're welcome! Let me know if you need anything else.",
            f"My pleasure, {name}! You are welcome! Feel free to ask more questions."
        ]
        return random.choice(responses)

    if re.search(r'\b(who are you|what is your name|your name)\b', text):
        return (f"I am Smart AI Chatbot! 🤖 A rule-based conversational system created as a "
                f"B.Tech AI Minor Project to assist you, {name}.")

    # --------------------------------------------------------------------------
    # 4. DATE AND TIME INTENTS
    # --------------------------------------------------------------------------
    if re.search(r'\b(date|today|day)\b', text) and not re.search(r'\b(update)\b', text):
        return f"📅 Today's date is **{get_current_date()}**."

    if re.search(r'\b(time|clock)\b', text):
        return f"🕒 The current time is **{get_current_time()}**."

    # --------------------------------------------------------------------------
    # 5. ARITHMETIC / CALCULATION INTENT
    # --------------------------------------------------------------------------
    # Detects math keywords or expressions containing numbers and operators
    if re.search(r'\b(calculate|compute|math|add|subtract|multiply|divide)\b', text) or re.search(r'\d+\s*[\+\-\*\/\%\^]\s*\d+', text):
        return safe_calculate(text)

    # --------------------------------------------------------------------------
    # 6. JOKES AND FACTS INTENTS
    # --------------------------------------------------------------------------
    if re.search(r'\b(joke|funny|laugh|humor)\b', text):
        return f"😄 Here is a joke for you, {name}:\n\n{random.choice(JOKES)}"

    if re.search(r'\b(fact|facts|trivia|interesting)\b', text):
        return f"💡 **AI Fact**: {random.choice(AI_FACTS)}"

    # --------------------------------------------------------------------------
    # 7. ARTIFICIAL INTELLIGENCE KNOWLEDGE BASE INTENTS
    # --------------------------------------------------------------------------
    if re.search(r'\b(what is ai|definition of ai|explain ai|artificial intelligence)\b', text):
        return ("🤖 **Artificial Intelligence (AI)** is a branch of Computer Science dedicated to building "
                "smart systems capable of performing tasks that typically require human intelligence, "
                "such as decision-making, pattern recognition, learning, and visual perception.")

    if re.search(r'\b(machine learning|what is ml|explain ml)\b', text):
        return ("🧠 **Machine Learning (ML)** is a subfield of AI that enables systems to automatically "
                "learn and improve from experience without being explicitly programmed. It uses statistical "
                "algorithms to find patterns in data.")

    if re.search(r'\b(deep learning|what is dl|neural network)\b', text):
        return ("🔬 **Deep Learning** is a subset of Machine Learning based on Artificial Neural Networks with "
                "multiple layers (hence 'deep'). It excels at processing unstructured data like images, audio, and text.")

    if re.search(r'\b(nlp|natural language processing)\b', text):
        return ("💬 **Natural Language Processing (NLP)** is a domain of AI that focuses on enabling computers "
                "to understand, analyze, interpret, and generate human languages naturally.")

    # --------------------------------------------------------------------------
    # 8. PYTHON KNOWLEDGE BASE INTENTS
    # --------------------------------------------------------------------------
    if re.search(r'\b(who created python|inventor of python|father of python|who made python)\b', text):
        return ("🐍 **Python** was created by **Guido van Rossum** and released in **1991**. "
                "He designed it with an emphasis on code readability and clean syntax!")

    if re.search(r'\b(what is python|explain python|about python)\b', text):
        return ("🐍 **Python** is a high-level, interpreted, general-purpose programming language. "
                "It is renowned for its easy-to-read syntax, dynamic typing, and vast collection of libraries "
                "making it ideal for AI, Data Science, Web Development, and Automation.")

    if re.search(r'\b(why python for ai|python in ai|python ai)\b', text):
        return ("⭐ Python is popular in AI because of:\n"
                "1. Clean and simple syntax.\n"
                "2. Huge ecosystem of AI/ML frameworks (TensorFlow, PyTorch, Scikit-Learn).\n"
                "3. Strong global community support.")

    if re.search(r'\b(data types|python data types)\b', text):
        return ("📊 Built-in Python Data Types include:\n"
                "- Numeric: `int`, `float`, `complex`\n"
                "- Text: `str`\n"
                "- Sequence: `list`, `tuple`, `range`\n"
                "- Mapping: `dict`\n"
                "- Set: `set`, `frozenset`\n"
                "- Boolean: `bool`")

    # --------------------------------------------------------------------------
    # 9. UNKNOWN / FALLBACK INTENT (POLITE RESPONDER)
    # --------------------------------------------------------------------------
    fallbacks = [
        f"I'm sorry, {name}, I didn't quite understand that. 😅\n"
        f"Try asking me about **AI**, **Python**, **Date/Time**, **Calculations**, or type '**help**' for a list of topics!",

        f"Hmm, that query is outside my current knowledge base, {name}.\n"
        f"You can ask me questions like 'What is Machine Learning?', 'Calculate 50 * 3', or 'Tell me a joke'.",

        f"I am a rule-based AI chatbot and couldn't match your query, {name}.\n"
        f"Type '**help**' to view supported commands and sample questions!"
    ]
    return random.choice(fallbacks)


# ==============================================================================
# MAIN EXECUTION LOOP & INTERACTIVE UI
# ==============================================================================

def print_banner():
    """Prints a styled CLI banner."""
    print("=" * 72)
    print("                🤖 SMART AI CHATBOT (Python Standard Library)         ")
    print("                     B.Tech AI Minor Project Submission               ")
    print("=" * 72)


def run_chatbot():
    """
    Main driver function. Initializes state, greets user, prompts for name,
    and runs the interactive chat loop until the user exits.
    """
    print_banner()
    state = ChatState()

    # Step 1: Initial Welcome & Name Prompt
    print("\nBot: Hello! Welcome to the Smart AI Chatbot system.")
    try:
        user_name_input = input("Bot: May I know your name, please? ").strip()
        if user_name_input:
            state.set_user_name(user_name_input)
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye!")
        sys.exit(0)

    # Step 2: Personalized Welcome & Instructions
    print(f"\nBot: Nice to meet you, {state.user_name}! 👋")
    print(f"Bot: Type 'help' to see what I can do, or type 'bye' to exit.\n")
    print("-" * 72)

    # Step 3: Interactive Chat Loop
    while state.is_active:
        try:
            user_input = input(f"\n{state.user_name}: ").strip()

            # Skip empty inputs
            if not user_input:
                continue

            state.increment_conversation()

            # Check for exit intent
            if match_exit(user_input):
                print(f"\nBot: Goodbye, {state.user_name}! It was a pleasure talking with you. Have a great day! 👋 🤖")
                print("=" * 72)
                state.is_active = False
                break

            # Process intent & obtain response
            response = process_response(user_input, state)
            print(f"\nBot: {response}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\nBot: Program interrupted. Goodbye, {state.user_name}! 👋")
            break


# Script Entry Point
if __name__ == "__main__":
    run_chatbot()

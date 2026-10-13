# Task 1 - Rule based chatbot
# Matches what the user types against a list of regex patterns and
# replies with a canned response. No ML involved, just pattern matching.

import random
import re
from datetime import datetime

BOT_NAME = "Buddy"
EXIT_PATTERN = r"^(?:bye|goodbye|exit|quit|see you)[.!?]*$"

# each rule is (pattern, list of possible replies)
# order matters: the first pattern that matches wins, so specific ones go first
RULES = [
    (r"my name is (\w+)",
     ["Nice to meet you, {0}!", "Hey {0}, good to meet you."]),

    (EXIT_PATTERN,
     ["Bye! Take care.", "See you later!", "Goodbye, have a good one."]),

    (r"\b(hi|hello|hey|namaste|hola)\b",
     ["Hello! How can I help you?", "Hey there! What's up?", "Hi! Ask me something."]),

    (r"how are you|how r u|how's it going",
     ["I'm doing fine, thanks for asking. How about you?",
      "All good on my side! You?"]),

    (r"(what('s| is) your name|who are you)",
     [f"I'm {BOT_NAME}, a small rule-based chatbot.",
      f"They call me {BOT_NAME}. I live inside a Python script."]),

    (r"\b(time|clock)\b",
     ["__TIME__"]),

    (r"\b(date|day|today)\b",
     ["__DATE__"]),

    (r"\b(thanks|thank you|thx)\b",
     ["No problem!", "Anytime.", "Happy to help."]),

    (r"(what can you do|help)",
     ["I can chat a little, tell you the time or date, and answer a few "
      "questions about programming and AI. Try asking 'what is python' or 'what is AI'."]),

    (r"\bwhat is (python)\b",
     ["Python is a high level programming language known for readable syntax. "
      "It's very popular for AI and data science."]),

    (r"\bwhat is (ai|artificial intelligence)\b",
     ["AI is about making machines do tasks that normally need human "
      "intelligence, like understanding language or recognising images."]),

    (r"\bwhat is (ml|machine learning)\b",
     ["Machine learning is a part of AI where models learn patterns from data "
      "instead of being explicitly programmed."]),

    (r"(joke|funny)",
     ["Why do programmers prefer dark mode? Because light attracts bugs.",
      "There are 10 kinds of people: those who know binary and those who don't."]),

    (r"(i am|i'm) (sad|tired|bored|stressed)",
     ["Sorry to hear you're feeling {1}. Maybe take a short break?",
      "That happens to all of us. Want to hear a joke?"]),
]

FALLBACKS = [
    "Hmm, I didn't get that. Can you say it differently?",
    "I'm not sure what you mean. Type 'help' to see what I can do.",
    "Sorry, I only know a few things. Try asking something else.",
]


def get_reply(user_text):
    text = user_text.lower().strip()

    for pattern, replies in RULES:
        match = re.search(pattern, text)
        if match:
            reply = random.choice(replies)
            if reply == "__TIME__":
                return "It's " + datetime.now().strftime("%I:%M %p") + " right now."
            if reply == "__DATE__":
                return "Today is " + datetime.now().strftime("%A, %d %B %Y") + "."
            # fill in captured groups like the user's name
            groups = match.groups()
            if "my name is" in pattern:
                groups = [g.capitalize() for g in groups]   # garv -> Garv
            return reply.format(*groups)

    return random.choice(FALLBACKS)


def main():
    print(f"{BOT_NAME}: Hi, I'm {BOT_NAME}. Type 'bye' to leave.")
    while True:
        try:
            user_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_text.strip():
            continue

        reply = get_reply(user_text)
        print(f"{BOT_NAME}: {reply}")

        if re.search(EXIT_PATTERN, user_text.lower().strip()):
            break


if __name__ == "__main__":
    main()

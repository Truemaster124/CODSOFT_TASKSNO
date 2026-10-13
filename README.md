# CodSoft AI Tasks

Three small Python projects for the CodSoft Artificial Intelligence internship: a rule-based chatbot, a Tic-Tac-Toe opponent, and a movie recommender.

All three run in the terminal using Python 3 and the standard library. No extra packages or dataset downloads are needed.

## Run the projects

```bash
git clone https://github.com/Truemaster124/CODSOFT_TASKSNO.git
cd CODSOFT_TASKSNO

python task1_chatbot/chatbot.py
python task2_tictactoe/tictactoe.py
python task4_recommender/recommender.py
```

Run one script at a time. If your system uses `python3` or `py` instead of `python`, use that command.

## Task 1: Rule-based chatbot

Buddy matches messages against regular expressions and chooses a response from the first matching rule. It can handle greetings, introductions, time and date questions, and a few questions about Python and AI.

Try `hi, my name is Garv`, `what is AI`, or `tell me a joke`. Enter `bye` to exit.

The rules are deliberately simple. The bot does not learn from conversations or remember your name between messages. Anything outside its rules gets a fallback response.

## Task 2: Tic-Tac-Toe

You play as X and the computer plays as O. Choose who starts, then enter a board position from 1 to 9.

The computer uses minimax with alpha-beta pruning. It scores possible game outcomes and prefers a quick win over a later one. With correct play, you can draw against it; it should not lose. The tests check every possible human move sequence against its chosen moves, with either player starting.

## Task 4: Movie recommendations

The recommender uses 20 movies and ratings from eight fictional users. Its menu offers two approaches:

- **Similar movies:** represents genres as binary vectors and compares them using cosine similarity. Try `Inception`.
- **Recommendations for a user:** finds up to three users with similar rating vectors, then uses a weighted average to rank movies the selected user has not rated. Try `Aman`.

This is a small demonstration dataset. Genre matching ignores plot, cast, and writing style. Collaborative filtering treats missing ratings as zero in the similarity calculation and does not adjust for users who tend to rate everything highly. Predicted ratings are examples, not measured recommendation accuracy.

## Checks

```bash
python -m unittest discover -s tests -v
```

The checks cover chatbot matching, invalid game input, Tic-Tac-Toe outcomes, cosine similarity, and recommendation filtering.

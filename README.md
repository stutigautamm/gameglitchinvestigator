# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.

This is a Streamlit-based interactive number guessing game. Players select a difficulty (Easy, Normal, or Hard), which determines the range of numbers and the number of attempts they are allowed. The player submits guesses and receives "Higher" or "Lower" hints, and their final score is calculated based on how many wrong guesses they made before finding the secret number.

- [ ] Detail which bugs you found.
Mismatched Hints: The game logic told the player to go "Higher" when they actually needed to go "Lower" and vice versa.

Out-of-Bounds Typo Bug: The original code punished players for accidentally typing text or numbers outside the difficulty boundaries, wasting their attempts.

Points/Score Bug: The scoring math penalized the player live during the game and subtracted points again at the end, resulting in an unfair final score.

"New Game" Button Broken: The original new_game button did not work as intended where it didn't reset everything and let the player start a new game.

Hardcoded Number Ranges: Even if a player selected "Easy" (1 to 20), the main screen would show 1 and 100, and the new secret number being generated would also be between 1 and 100, completely ignoring the difficulty settings.

Scoring/Points System: The logic didn't make sense for the amount of points being rewarded at the end of the games. 

- [ ] Explain what fixes you applied.

Reversed the greater-than/less-than logic inside check_guess so the hints point in the correct mathematical direction.

Updated parse_guess to require minimum and maximum boundaries, explicitly rejecting letters, empty strings, and out-of-bounds numbers without incrementing the attempt counter.

Updated the if new_game: block to dynamically generate the secret number using the active low and high difficulty variables instead of a hardcoded 1 and 100 and made sure the app reset st.session_state.status = "playing" and st.session_state.history = {} for the button to work.

Refactored the math inside update_score to use a clean "Calculate at the End" method, keeping the score at 0 until the player wins, then awarding a flat 100 points minus 5 points per previous wrong guess.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "Normal" difficulty (Range: 1 to 50, 7 attempts) from the sidebar.
2. User enters a guess of 25 and clicks "Submit Guess".
3. Game returns a yellow warning hint: "Go HIGHER!" (Attempts left drops to 6).
4. User enters a guess of 40 and clicks "Submit Guess".
5. Game returns a yellow warning hint: "Go LOWER!" (Attempts left drops to 5).
6. User enters a guess of 32 and correctly guesses the secret number.
7. Game displays a green success message ("Correct!"), triggers screen balloons, and displays the final calculated score of 90.
8. The user clicks "New Game" if they want to start again. 

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================

============================= test session starts =============================
platform win32 -- Python 3.13.12, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Stuti\AI110\gameglitchinvestigator
plugins: anyio-4.13.0
collected 15 items

tests\test_game_logic.py ...............                                 [100%]

============================= 15 passed in 0.04s ==============================

```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

import random

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    #FIX: Corrected range values so progression goes from easiest (1-20) to hardest (1-100)
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50

def parse_guess(raw: str):
    # FIX: Added .strip() to cleanly handle whitespace inputs
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a valid integer."

    return True, value, None

def check_guess(guess: int, secret: int):
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Swapped hint directions so 'Too High' tells you to go LOWER and vice versa
    # FIX: Stripped out the dangerous try/except string fallbacks completely
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"

def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Standardized penalty reduction instead of the glitchy modulo score addition formula
    if outcome in ["Too High", "Too Low"]:
        return current_score - 5

    return current_score
import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")

def test_difficulty_ranges():
    # Corrected range values so progression goes from easiest to hardest
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
    
    # Fallback/default check
    assert get_range_for_difficulty("Unknown") == (1, 50)

def test_parse_guess_empty_or_whitespace():
    # Added .strip() to cleanly handle whitespace inputs
    ok, val, err = parse_guess("", 1, 20)
    assert not ok
    assert err == "Enter a guess."

    ok, val, err = parse_guess("   ", 1, 20)
    assert not ok
    assert err == "Enter a guess."

    ok, val, err = parse_guess(None, 1, 20)
    assert not ok
    assert err == "Enter a guess."

def test_parse_guess_invalid_types():
    # Catch exceptions for non-integer strings
    ok, val, err = parse_guess("abc", 1, 20)
    assert not ok
    assert err == "That is not a valid integer."

    ok, val, err = parse_guess("12a", 1, 20)
    assert not ok
    assert err == "That is not a valid integer."

def test_parse_guess_out_of_bounds():
    # Reject guesses that fall outside the active difficulty boundaries
    ok, val, err = parse_guess("21", 1, 20)
    assert not ok
    assert err == "Your guess must be between 1 and 20."

    ok, val, err = parse_guess("0", 1, 20)
    assert not ok
    assert err == "Your guess must be between 1 and 20."

def test_parse_guess_valid():
    # Valid guess inside bounds
    ok, val, err = parse_guess("15", 1, 20)
    assert ok
    assert val == 15
    assert err is None

    # Handles floats cast to ints
    ok, val, err = parse_guess("15.9", 1, 20)
    assert ok
    assert val == 15
    assert err is None

def test_check_guess_win():
    # Winning condition
    outcome, msg = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct!" in msg

def test_check_guess_too_high():
    # Swapped hint directions so 'Too High' tells you to go LOWER
    outcome, msg = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in msg

def test_check_guess_too_low():
    # Swapped hint directions so 'Too Low' tells you to go HIGHER
    outcome, msg = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in msg

def test_check_guess_no_string_fallback():
    # Passing a string should properly throw a TypeError instead of silently failing.
    with pytest.raises(TypeError):
        check_guess("50", 40)

def test_update_score_penalties():
    # FIX: "Calculate at the End" method means live penalties do nothing to the score!
    assert update_score(current_score=0, outcome="Too High", attempt_number=1) == 0
    assert update_score(current_score=0, outcome="Too Low", attempt_number=2) == 0

def test_update_score_win():
    # FIX: Win on Attempt 1 awards a perfect 100. (100 - 5 * 0)
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 100
    
    # FIX: Win on Attempt 3 awards 90 points. (100 - 5 * 2)
    assert update_score(current_score=0, outcome="Win", attempt_number=3) == 90

def test_update_score_win_clamp():
    # Minimum points awarded for a win should be clamped to 10 if attempt_number is very high
    # Attempt 25 -> 100 - 5 * (24) = -20 -> clamped to 10.
    assert update_score(current_score=0, outcome="Win", attempt_number=25) == 10
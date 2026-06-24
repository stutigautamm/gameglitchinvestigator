import random
import streamlit as st
import logic_utils

# FIX: Refactored game logic into logic_utils.py using agent mode
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# FIX: Balanced attempts and mapped them to the corrected logical difficulties
attempt_limit_map = {
    "Easy": 6,
    "Normal": 7,
    "Hard": 8,
}
attempt_limit = attempt_limit_map[difficulty]

# FIX: Added required module prefix to resolve NameError
low, high = logic_utils.get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Track current difficulty using .get() to prevent KeyError on first load.
# FIX: Force a new secret number generation and reset all state variables if difficulty changes mid-game.
if "secret" not in st.session_state or st.session_state.get("current_difficulty") != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.score = 0  # FIX: Ensures the score zeroes out if the difficulty is changed mid-game
    st.session_state.history = {} # FIX: Converted history to a dictionary to fix the 0-index display bug
    st.session_state.status = "playing"

# FIX: Cleaned up duplicate initializations. Attempts start at 0 so the first guess cleanly registers as Attempt 1
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = {}

st.subheader("Make a guess")

# FIX: Created empty placeholders to reserve space in the layout.
# This prevents the "UI lag" bug because we can populate these boxes AFTER the logic runs!
info_container = st.empty()
debug_container = st.empty()

# FIX/RESTORE: Reverted back to the original starter-code layout without the st.form wrapper
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Expanded reset block to completely wipe stale history and game-over states
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0  
    st.session_state.secret = random.randint(low, high) 
    st.session_state.status = "playing"                 
    st.session_state.history = {}                
    st.success("New game started.")
    st.rerun()

# FIX: Added 'and st.session_state.status == "playing"' to completely lock out Zombie Submissions!
if submit and st.session_state.status == "playing":
    # FIX: Passed low and high bounds to parse_guess so it can validate the range
    ok, guess_int, err = logic_utils.parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: We NO LONGER increment attempts or save to history if the input is an invalid string!
        st.error(err)
    else:
        # FIX: Safely increment attempts only for valid integer guesses
        st.session_state.attempts += 1
        
        # FIX: Save to dictionary using the attempt number as the key, forcing the display to start at 1 instead of 0
        st.session_state.history[st.session_state.attempts] = guess_int

        secret = st.session_state.secret

        outcome, message = logic_utils.check_guess(guess_int, secret)

        if show_hint:
            if outcome == "Win":
                st.success(message)
            else:
                st.warning(message)

        st.session_state.score = logic_utils.update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FIX: We now fill the containers down here so the UI perfectly reflects immediate state updates!
info_container.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with debug_container.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
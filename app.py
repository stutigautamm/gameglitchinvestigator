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
    st.session_state.history = []
    st.session_state.status = "playing"

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIX: Created empty placeholders to reserve space in the layout.
# This fixes the "UI lag" bug because we can now populate these boxes AFTER the state updates at the bottom!
info_container = st.empty()
debug_container = st.empty()

# FIX: Wrapped the text input and submit button inside an st.form. 
# This completely prevents Streamlit's double-refresh bug by batching the text input and button click into a single execution!
with st.form(key=f"guess_form_{difficulty}"):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

# FIX: Moved New Game and Hint toggles outside the form so they don't accidentally trigger a form submission
col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Expanded reset block to completely wipe stale history and game-over states
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0  # FIX: Forces the score to reset completely when clicking "New Game"
    st.session_state.secret = random.randint(low, high) # FIX: Generated secret using actual difficulty bounds instead of hardcoded 100
    st.session_state.status = "playing"                 # FIX: Resets game status to unlock input
    st.session_state.history = []                       # FIX: Clears the previous game's history array
    st.success("New game started.")
    st.rerun()

if submit:
    st.session_state.attempts += 1

    # FIX: Added required module prefix to resolve NameError
    ok, guess_int, err = logic_utils.parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: Removed the buggy even-attempt string conversion block that caused type errors
        secret = st.session_state.secret

        # FIX: Added required module prefix to resolve NameError
        outcome, message = logic_utils.check_guess(guess_int, secret)

        if show_hint:
            # FIX: Display the winning message in a green success box instead of a yellow warning box
            if outcome == "Win":
                st.success(message)
            else:
                st.warning(message)

        # FIX: Added required module prefix to resolve NameError
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

# FIX: We now fill the containers down here. Because this runs AFTER the submit logic, 
# the UI perfectly reflects the immediate, up-to-date Attempt and Score numbers without requiring a double-click!
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

# FIX: Added 'if not submit:' to safely lock the game inputs if it is over, avoiding duplicate screen messages on the exact frame the game ends
if st.session_state.status != "playing":
    if not submit: 
        if st.session_state.status == "won":
            st.success("You already won. Start a new game to play again.")
        else:
            st.error("Game over. Start a new game to try again.")
    st.stop()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The first time I ran the game it looked like a standard, clean Streamlit application, but it did not really work as intended. The UI text for the range of the number I was supposed to guess was immediately misleading, contradicting the difficulty settings I selected in the sidebar. Furthermore, when I tried to actually play, the hints were confusing as well as they suggested the opposite of what they should. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
One concrete bug I noticed was that the instruction box text on the main screen is hardcoded to say "Guess a number between 1 and 100" even if you change the difficulty to easy or hard (which should be 1 to 20 or 1 to 50). Another concrete bug was that even when you set the difficulty to "Easy", the "New game" button generates a number between 1 to 100, not 1 to 20 as it should. I also noticed the New Game button was not working properly. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                       |       Expected Behavior            |       Actual Behavior              | Console Output / Error |
|-----------------------------|------------------------------------|------------------------------------|------------------------|
| Change difficulty to "Easy" | The main page should say "Guess a  | Still says "Guess a number between |  None                  |
|                             | number between 1 and 20."          | 1 and 100."                        |                        |
|--------------------------------------------------------------------------------------------------------------------------------|
| Change difficulty to "Easy" | Secret number should be generated  | Secret number sometimes generates  |  None                  |
| and click "New Game"        | between 1 and 20.                  | a number higher than 20            |                        |
|--------------------------------------------------------------------------------------------------------------------------------|
| Lose all game attempts and  | Be allowed to guess again and have | The "Game over. Start a new game   | None                   |
| click New Game              | your lives restored                | to try again." message remains and |                        |
|                             |                                    | game refuses to accept inputs.     |                        |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude and Gemini Pro. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
The AI correctly noted that the original initialization block set st.session_state.attempts = 1 before any guess was made, which broke the UI calculation because the game app immediately added another attempt when the button was pushed. It suggested starting the attempt tracker at 0 instead so that the first guess accurately registered as attempt number one. I verified this by keeping the "Developer Debug Info" expander open while making my first guess and watching the counter correctly flip from 0 to 1.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
At one point, the AI suggested 
The AI originally suggested a scoring formula of 100 - 10 * (attempt_number) for a winning guess to calculate a sliding scale of points. This was a misleading logic because the app was already deducting 5 points for every wrong guess on the screen, meaning the player was still being punished twice for the same mistake. I verified this visually when an Attempt 2 win calculated out to an unfair score of 75 instead of a clean 95, prompting me to change it to a flat 100-point reward instead.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was fully fixed when both the UI and the underlying math worked correctly under edge-case conditions. For example, I wouldn't just check if the score looked right on a standard win, I would intentionally try to break it by submitting negative numbers, typing letters, and obeserving the "Developer Debug Info" expander making sure the attempts are being incremented correctly. Finally, running my automated pytest suite and seeing a 100% pass rate gave me the confidence that the core logic was truly solid and wouldn't break again.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
I ran a manual test where I intentionally typed the word "hello" into the guess box instead of a number. In the original starter code, this would take up one of my attempts and be counted in the attempt history. After my fix, the test proved my code worked because it properly caught the error, warned me, and kept my attempt counter frozen. I also ran pytest for test_parse_guess_invalid_types, which explicitly checked for letters/strings. I also ran a manual test where I guessed a number higher than the secret number, where it told me to go higher. This proved that the hints being given were backwards. 

- Did AI help you design or understand any tests? How?
Yes, the AI helped me design the specific test_update_score_win pytest function to verify our newly fixed scoring math. Since I changed the game to use a "Calculate at the End" method, the AI showed me how to write assertions that simulated an exact, late-game state. For example, it explained how passing current_score=0, outcome="Win", and attempt_number=3 should explicitly assert a final score of exactly 90 points, proving that the logic accurately deducted 5 points for the two previous wrong guesses.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I would explain that Streamlit is incredibly forgetful, like every time you click a button or type something into a box, it basically reloads the entire script from top to bottom and erases all its short-term memory. To fix this, you have to use st.session_state, which acts like a secure backpack. You put your important variables (like the current score, the attempt limit, or the secret number) into that backpack so they survive the constant page reloads and don't reset to zero.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I want to keep using the strategy of ruthlessly stress-testing edge cases, like trying to break a form with out-of-bounds numbers or invalid text inputs. Relying solely on the "happy path" where everything goes right hides massive bugs. I also plan to continue building isolated pytest functions for my math logic so I can verify my formulas without clicking through a UI a bunch of times.
  
- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I will be much more critical of the mathematical formulas and conditional logic the AI suggests right from the start. I realized that the AI is great at writing code that runs without syntax errors, but it can easily invent rules that make no logical sense in the context of the game's actual rules. I will map out the math on paper before blindly trusting the AI's equations.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project taught me that AI is an assistant, not a senior developer. It will confidently introduce subtle logical flaws if you aren't paying close enough attention, which might introduce even more bugs that you didn't have before. It proved to me that human QA testing, critical thinking, and understanding the code line-by-line are still necessary to building functional software.
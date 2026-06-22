# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
The game did not work as intended and there were a lot of bugs that needed to be fixed. One concrete bug I noticed was that the instruction box text on the main screen is hardcoded to say "Guess a number between 1 and 100" even if you change the difficulty to easy or hard (which should be 1 to 20 or 1 to 50). Another concrete bug was that even when you set the difficulty to "Easy", the "New game" button generates a number between 1 to 100, not 1 to 20 as it should. 

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
I used Claude and Gemini. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?


- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.


- Did AI help you design or understand any tests? How?


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

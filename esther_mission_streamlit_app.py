
import streamlit as st
import random

# Mission Data
mission_data = [
    {
        "turn": 1,
        "event": "Mordecai appears in mourning.",
        "trivia": "Who raised Esther?",
        "choices": ["A) Haman", "B) Mordecai", "C) Ezra", "D) Ruth"],
        "correct": "B",
        "outcome_correct": "Message delivered safely.",
        "outcome_incorrect": "Message delay. Timeline +1."
    },
    {
        "turn": 2,
        "event": "Esther enters the throne room uninvited.",
        "trivia": "What tribe was Haman descended from?",
        "choices": ["A) Edom", "B) Egypt", "C) Amalek", "D) Babylon"],
        "correct": "C",
        "outcome_correct": "King trusts Esther. Favor +1.",
        "outcome_incorrect": "Favor drops to Neutral."
    },
    {
        "turn": 3,
        "event": "Esther hosts a banquet to buy time.",
        "trivia": "What did Mordecai uncover?",
        "choices": ["A) A forged decree", "B) A plot to poison him", "C) A plot to assassinate him", "D) A stolen royal seal"],
        "correct": "C",
        "outcome_correct": "King remembers Mordecai's loyalty.",
        "outcome_incorrect": "No recognition for Mordecai yet."
    },
    {
        "turn": 4,
        "event": "Esther suggests honoring Mordecai.",
        "trivia": "What did Haman build intending to hang Mordecai?",
        "choices": ["A) A stake", "B) A cross", "C) A pit", "D) A gallows"],
        "correct": "D",
        "outcome_correct": "Haman humiliated. Favor +1.",
        "outcome_incorrect": "Haman retains influence."
    },
    {
        "turn": 5,
        "event": "Esther uses Intercede and reveals Haman’s plot.",
        "trivia": "",
        "choices": [],
        "correct": "",
        "outcome_correct": "King commands Haman’s execution. Victory!",
        "outcome_incorrect": ""
    }
]

# Game state
if "turn" not in st.session_state:
    st.session_state.turn = 1
    st.session_state.timeline = 0
    st.session_state.favor = "Neutral"
    st.session_state.intercede_used = False
    st.session_state.game_over = False

st.title("Bible Realms: Esther Mission Simulation")

if st.session_state.turn <= len(mission_data):
    current = mission_data[st.session_state.turn - 1]
    st.header(f"Turn {st.session_state.turn}")
    st.subheader(current["event"])

    if current["trivia"]:
        st.markdown(f"**Trivia:** {current['trivia']}")
        answer = st.radio("Choose your answer:", current["choices"], key=f"trivia_{st.session_state.turn}")
        roll = st.button("Submit Turn")

        if roll:
            dice = random.randint(1, 6)
            st.markdown(f"🎲 You rolled a **{dice}**")

            if answer[0] == current["correct"]:
                st.success("Correct Answer!")
                st.info(current["outcome_correct"])
            else:
                st.error("Incorrect Answer!")
                st.warning(current["outcome_incorrect"])
                st.session_state.timeline += 1

            st.session_state.turn += 1
    else:
        st.success(current["outcome_correct"])
        st.session_state.turn += 1
else:
    st.header("Mission Complete!")
    if st.session_state.timeline < 6:
        st.success("🎉 Victory! The Jews were saved.")
    else:
        st.error("💀 Mission Failed. Haman's plot succeeded.")

    if st.button("Restart Mission"):
        st.session_state.turn = 1
        st.session_state.timeline = 0
        st.session_state.favor = "Neutral"
        st.session_state.intercede_used = False
        st.session_state.game_over = False

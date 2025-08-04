
import streamlit as st
import random

# --- Turn 1 Data ---
mission_data = [
    {
        "turn": 1,
        "event": "Mordecai appears in mourning.",
        "trivia": "Who raised Esther?",
        "choices": ["A) Haman", "B) Mordecai", "C) Ezra", "D) Ruth"],
        "correct": "B",
        "outcome_correct": "Esther receives Mordecai’s message. The plan to intercede begins.",
        "outcome_incorrect": "The message is delayed. Esther remains unaware. Timeline +1."
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

# --- Game Start ---
st.title("Bible Realms: Esther Mission Simulation")

# --- Initialize session state ---
if "ready" not in st.session_state:
    st.session_state.ready = False
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "timeline" not in st.session_state:
    st.session_state.timeline = 0
if "favor" not in st.session_state:
    st.session_state.favor = "Neutral"
if "intercede_used" not in st.session_state:
    st.session_state.intercede_used = False

# --- Mission Setup ---
if not st.session_state.ready:
    st.header("Mission Setup")
    st.markdown("""
    **You are Esther**, Queen of Persia, chosen for such a time as this.

    🎯 **Mission Objective**: Expose Haman's plot and save your people.  
    🕰️ **Timeline Limit**: 6 rounds  
    📊 **Attributes**:  
    - Faith: 5  
    - Courage: 7  
    - Wisdom: 4  
    - Obedience: 6  
    - Special Ability: Intercede (1 use only)
    """)
    if st.button("Begin Mission"):
        st.session_state.ready = True
        st.session_state.turn = 1
       
# --- Esther/Haman Summary Screen ---
elif st.session_state.turn == 1 and "summary_shown" not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Esther (chatGPT-Animation Creation).png", caption="Queen Esther", width=300)

    st.markdown("""
    ### Esther’s Rise
    Esther was a young Jewish orphan raised by her cousin Mordecai. When Queen Vashti refused to appear before King Xerxes (also known as Ahasuerus) during a royal banquet, the king removed her from her position and launched a search for a new queen.

    Esther was taken to the palace and, after undergoing a 12-month beautification process, she was presented to the king. He was more pleased with Esther than any of the others and crowned her queen. At Mordecai’s instruction, Esther kept her Jewish identity secret.

    While stationed at the king’s gate, Mordecai overheard a plot by two royal officials—Bigthan and Teresh—to assassinate the king. He informed Esther, who passed the warning to Xerxes. After an investigation, the plot was confirmed, and the conspirators were executed. Mordecai’s act of loyalty was recorded in the royal chronicles, though no reward was given at the time.
    """)

    st.image("Haman (Copilot).png", caption="Haman the Agagite", width=300)
    st.markdown("""
    ### Haman’s Plot Against the Jews
    Not long after Esther became queen, King Xerxes elevated a man named Haman the Agagite to a high position of authority. All royal officials were ordered to honor him, but Mordecai refused to bow, as a Jew loyal only to God.

    Infuriated, Haman sought revenge—not just on Mordecai, but on all Jews throughout the empire. He convinced Xerxes to issue a royal decree to annihilate every Jew, young and old, on a specific day. The king agreed, unaware of Esther’s heritage, and sealed it with his signet ring.

    When Mordecai learned of the decree, he tore his clothes, put on sackcloth and ashes, and went into public mourning. He sent word to Esther, urging her to go before the king and plead for her people’s lives—despite the risk of death for appearing uninvited.
    """)

    if st.button("Continue to Turn 1"):
        st.session_state.turn += 1
else:
    if st.session_state.turn <= len(mission_data):
        current = mission_data[st.session_state.turn - 1]
        st.header(f"Turn {st.session_state.turn}")
        st.subheader(current["event"])

        if f"submitted_{st.session_state.turn}" not in st.session_state:
            if current["trivia"]:
                st.markdown(f"**Trivia:** {current['trivia']}")
                answer = st.radio("Choose your answer:", current["choices"], key=f"trivia_{st.session_state.turn}")
                if st.button("Submit Answer"):
                    dice = random.randint(1, 6)
                    st.markdown(f"🎲 You rolled a **{dice}**")

                    if answer[0] == current["correct"]:
                        st.success("Correct Answer!")
                        st.info(current["outcome_correct"])
                    else:
                        st.error("Incorrect Answer!")
                        st.warning(current["outcome_incorrect"])
                        st.session_state.timeline += 1

                    st.session_state[f"submitted_{st.session_state.turn}"] = True
            else:
                st.success(current["outcome_correct"])
                st.session_state[f"submitted_{st.session_state.turn}"] = True

        if f"submitted_{st.session_state.turn}" in st.session_state:
            if st.button("Next"):
                st.session_state.turn += 1
    else:
        st.header("Mission Complete!")
        if st.session_state.timeline < 6:
            st.success("🎉 Victory! The Jews were saved.")
        else:
            st.error("💀 Mission Failed. Haman's plot succeeded.")

        if st.button("Restart Mission"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

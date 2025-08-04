import streamlit as st
import random

mission_data = [
    {
        "turn": 1,
        "event": "Mordecai appears at the gate in sackcloth.",
        "trigger": "He’s mourning, and you sense something is wrong. You send Hathach to find out more.",
        "task": {
            "type": "challenge",
            "stat": "wisdom",
            "required_total": 8,
            "modifier": 4,
            "success_text": "You sense urgency and send Hathach to investigate.",
            "failure_text": "You hesitate, delaying Hathach’s mission. Timeline +1."
        },
        "trivia": {
            "question": "Who raised Esther?",
            "choices": ["A) Haman", "B) Mordecai", "C) Ezra", "D) Ruth"],
            "correct": "B",
            "outcome_correct": "Message delivered safely. Plan to intercede begins.",
            "outcome_incorrect": "Message delayed. Esther remains unaware. Timeline +1."
        }
    },
    {
        "turn": 2,
        "event": "Esther enters the throne room uninvited.",
        "trivia": {
            "question": "What tribe was Haman descended from?",
            "choices": ["A) Edom", "B) Egypt", "C) Amalek", "D) Babylon"],
            "correct": "C",
            "outcome_correct": "King trusts Esther. Favor +1.",
            "outcome_incorrect": "Favor drops to Neutral."
        }
    },
    {
        "turn": 3,
        "event": "Esther hosts a banquet to buy time.",
        "trivia": {
            "question": "What did Mordecai uncover?",
            "choices": ["A) A forged decree", "B) A plot to poison him", "C) A plot to assassinate him", "D) A stolen royal seal"],
            "correct": "C",
            "outcome_correct": "King remembers Mordecai's loyalty.",
            "outcome_incorrect": "No recognition for Mordecai yet."
        }
    },
    {
        "turn": 4,
        "event": "Esther suggests honoring Mordecai.",
        "trivia": {
            "question": "What did Haman build intending to hang Mordecai?",
            "choices": ["A) A stake", "B) A cross", "C) A pit", "D) A gallows"],
            "correct": "D",
            "outcome_correct": "Haman humiliated. Favor +1.",
            "outcome_incorrect": "Haman retains influence."
        }
    },
    {
        "turn": 5,
        "event": "Esther uses Intercede and reveals Haman’s plot.",
        "trivia": None,
        "outcome_correct": "King commands Haman’s execution. Victory!"
    }
]

# --- Game Start ---
st.title("Bible Realms: Esther Mission Simulation")

# --- Initialize session state ---
if "ready" not in st.session_state:
    st.session_state.ready = False
if "turn" not in st.session_state:
    st.session_state.turn = 0  # Start at turn 0 to show summary
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
        st.session_state.turn = 0

# --- Show Summary at Turn 0 ---
elif st.session_state.turn == 0:
    # --- Esther’s Rise ---
    st.subheader("Esther’s Rise")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Esther was a young Jewish orphan raised by her cousin Mordecai. When Queen Vashti refused to appear before King Xerxes (also known as Ahasuerus) during a royal banquet, the king removed her from her position and launched a search for a new queen.

        Esther was taken to the palace and, after undergoing a 12-month beautification process, she was presented to the king. He was more pleased with Esther than any of the others and crowned her queen. At Mordecai’s instruction, Esther kept her Jewish identity secret.

        While stationed at the king’s gate, Mordecai overheard a plot by two royal officials—Bigthan and Teresh—to assassinate the king. He informed Esther, who passed the warning to Xerxes. After an investigation, the plot was confirmed, and the conspirators were executed. Mordecai’s act of loyalty was recorded in the royal chronicles, though no reward was given at the time.
        """)
    with col2:
        st.image("Esther (chatGPT-Animation Creation).png", caption="Queen Esther", width=250)

    # --- Haman’s Plot ---
    st.subheader("Haman’s Plot Against the Jews")
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown("""
        Not long after Esther became queen, King Xerxes elevated a man named Haman the Agagite to a high position of authority. All royal officials were ordered to honor him, but Mordecai refused to bow, as a Jew loyal only to God.

        Infuriated, Haman sought revenge—not just on Mordecai, but on all Jews throughout the empire. He convinced Xerxes to issue a royal decree to annihilate every Jew, young and old, on a specific day. The king agreed, unaware of Esther’s heritage, and sealed it with his signet ring.

        When Mordecai learned of the decree, he tore his clothes, put on sackcloth and ashes, and went into public mourning. He sent word to Esther, urging her to go before the king and plead for her people’s lives—despite the risk of death for appearing uninvited.
        """)
    with col4:
        st.image("Haman (Copilot).png", caption="Haman the Agagite", width=250)

    if st.button("Continue to Turn 1"):
        st.session_state.turn = 1
# --- Main Mission Loop ---
elif st.session_state.turn <= len(mission_data):
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

# --- Mission End ---
else:
    st.header("Mission Complete!")
    if st.session_state.timeline < 6:
        st.success("🎉 Victory! The Jews were saved.")
    else:
        st.error("💀 Mission Failed. Haman's plot succeeded.")

    if st.button("Restart Mission"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

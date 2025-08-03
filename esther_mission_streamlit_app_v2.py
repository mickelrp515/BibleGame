import streamlit as st
import random

# --- Mission Data ---
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
        "event": "Esther must decide whether to approach the king.",
        "context": "Esther 4:13–17 — Mordecai urges Esther to speak up, and Esther calls for a fast before acting.",
        "biblical_choice": "A",
        "decision_choices": {
            "A": {
                "text": "Fast and pray for 3 days with your people",
                "result": "Your people are strengthened in unity. Gain +1 Wisdom for the next challenge.",
                "effect": {"wisdom_bonus": 1},
                "biblical": True
            },
            "B": {
                "text": "March into the throne room immediately",
                "result": "A bold move! Courage check required (1d6 + Courage ≥ 10).",
                "check": "courage",
                "threshold": 10,
                "base": 7,
                "biblical": False,
                "outcome_if_failed": "The king is not ready to see you. Timeline +1."
            },
            "C": {
                "text": "Secretly ask Hathach to investigate Haman",
                "result": "You delay the risk but learn critical information. Timeline +1, but gain insight.",
                "effect": {"timeline": 1},
                "biblical": False
            },
            "D": {
                "text": "Write an anonymous letter to the king",
                "result": "The letter is ignored. No effect.",
                "biblical": False
            }
        }
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

# --- Game Setup ---
if "turn" not in st.session_state:
    st.session_state.turn = 0
    st.session_state.timeline = 0
    st.session_state.favor = "Neutral"
    st.session_state.ready = False
    st.session_state.alternate_timeline = False

st.title("Bible Realms: Esther Mission Simulation")

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

    Click below to begin your mission.
    """)
    if st.button("Begin Mission"):
        st.session_state.ready = True
        st.session_state.turn = 1

elif st.session_state.turn == 2:
    current = mission_data[1]
    st.header(f"Turn 2: {current['event']}")
    st.markdown(f"📖 **Context**: {current['context']}")
    st.subheader("Choose your next move:")

    choices = current["decision_choices"]
    choice_keys = [f"{k}) {v['text']}" for k, v in choices.items()]
    selected = st.radio("Your decision:", choice_keys, key="decision_turn2")

    if st.button("Submit Decision"):
        choice = selected[0]
        selected_outcome = choices[choice]

        if not selected_outcome.get("biblical", False):
            st.warning("⚠️ You have chosen a non-biblical path. An alternate timeline begins.")
            st.session_state.alternate_timeline = True

        st.markdown(f"📜 **Result**: {selected_outcome['result']}")

        if "check" in selected_outcome:
            roll = random.randint(1, 6)
            total = roll + selected_outcome.get("base", 0)
            st.markdown(f"🎲 You rolled {roll} + {selected_outcome['base']} = **{total}**")
            if total >= selected_outcome["threshold"]:
                st.success("✅ Check passed! You may proceed.")
            else:
                st.error("❌ Check failed.")
                st.markdown(selected_outcome.get("outcome_if_failed", "Timeline +1."))
                st.session_state.timeline += 1

        if "effect" in selected_outcome:
            for stat, val in selected_outcome["effect"].items():
                st.session_state[stat] = st.session_state.get(stat, 0) + val

        st.session_state[f"submitted_{st.session_state.turn}"] = True

    if f"submitted_{st.session_state.turn}" in st.session_state:
        if st.button("Next"):
            st.session_state.turn += 1

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

else:
    st.header("Mission Complete!")
    if st.session_state.alternate_timeline:
        st.warning("You created an alternate timeline. Replay for the biblical path!")
    if st.session_state.timeline < 6:
        st.success("🎉 Victory! The Jews were saved.")
    else:
        st.error("💀 Mission Failed. Haman's plot succeeded.")

    if st.button("Restart Mission"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

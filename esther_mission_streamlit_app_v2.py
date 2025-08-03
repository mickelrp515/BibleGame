
import streamlit as st
import random

# Initialize session state defaults
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

# Mission Data (excluding Turn 2)
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

# Game Setup Intro
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

else:
    # ✅ Custom TURN 2 logic
    if st.session_state.turn == 2:
        st.header("Turn 2: Prepare to Approach the King")
        st.subheader("Objective: Take your next step in response to Mordecai’s plea.")
        st.markdown("“Who knows but that you have come to your royal position for such a time as this?”")

        choices = {
            "A": {
                "text": "Fast and pray for 3 days with your people",
                "result": "Your people are strengthened in unity. Gain +1 Wisdom for the next challenge.",
                "effect": {"wisdom_bonus": 1}
            },
            "B": {
                "text": "March into the throne room immediately",
                "result": "A bold move! Courage check required (1d6 + Courage ≥ 10).",
                "check": "courage",
                "threshold": 10,
                "base": 7
            },
            "C": {
                "text": "Secretly ask Hathach to investigate Haman",
                "result": "You delay the risk but learn critical information. Timeline +1, but gain insight.",
                "effect": {"timeline": 1}
            },
            "D": {
                "text": "Write an anonymous letter to the king",
                "result": "The letter is ignored. No effect."
            }
        }

        selected = st.radio(
            "Choose your next move:",
            [f"{k}) {v['text']}" for k, v in choices.items()],
            key="turn2_decision"
        )

        if st.button("Submit Decision"):
            choice_key = selected[0]
            outcome = choices[choice_key]

            st.markdown(f"📜 **Result:** {outcome['result']}")

            if "check" in outcome:
                roll = random.randint(1, 6)
                base = outcome.get("base", 0)
                total = roll + base
                st.markdown(f"🎲 You rolled a {roll} + {base} = **{total}**")

                if total >= outcome["threshold"]:
                    st.success("✅ Courage check passed! You may proceed.")
                else:
                    st.error("❌ Courage check failed. The king is not ready to see you.")
                    st.session_state.timeline += 1

            if "effect" in outcome:
                for k, v in outcome["effect"].items():
                    st.session_state[k] = st.session_state.get(k, 0) + v

            st.session_state[f"submitted_{st.session_state.turn}"] = True

        if f"submitted_{st.session_state.turn}" in st.session_state:
            if st.button("Next"):
                st.session_state.turn += 1

    # ✅ All other turns
    elif st.session_state.turn <= len(mission_data) + 1:
        current = mission_data[st.session_state.turn - 1 if st.session_state.turn < 2 else st.session_state.turn - 2]
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

    # ✅ End of game
    else:
        st.header("Mission Complete!")
        if st.session_state.timeline < 6:
            st.success("🎉 Victory! The Jews were saved.")
        else:
            st.error("💀 Mission Failed. Haman's plot succeeded.")

        if st.button("Restart Mission"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

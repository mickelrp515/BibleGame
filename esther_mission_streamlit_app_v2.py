
import streamlit as st
import random

# --- Game Start ---
st.title("Bible Realms: Esther Mission Simulation")

if "ready" not in st.session_state:
    st.session_state.ready = False

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
        st.session_state.timeline = 0
        st.session_state.favor = "Neutral"
        st.session_state.intercede_used = False

# Now display the summaries AFTER the mission is initialized
if st.session_state.ready and st.session_state.turn == 1:
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

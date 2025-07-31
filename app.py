import streamlit as st
from modules.learner_logic import (
    determine_entry_point,
    deliver_lesson,
    handle_practice_attempt,
    get_next_question,
)

# ---------------------------
# STREAMLIT CONFIG
# ---------------------------
st.set_page_config(page_title="MyFuturePath MVP", layout="centered")

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "learner_profile" not in st.session_state:
    st.session_state.learner_profile = {
        "name": "",
        "history": {},  # topic -> status (mastered, needs review, paused)
        "current_subject": None,
        "current_topic": None,
    }

if "lesson" not in st.session_state:
    st.session_state.lesson = None

if "practice_state" not in st.session_state:
    st.session_state.practice_state = {
        "attempts": 0,
        "current_question": 0,
    }

if "show_next" not in st.session_state:
    st.session_state.show_next = False  # Control when to move to next topic

# ---------------------------
# UI: REGISTRATION PAGE
# ---------------------------
st.title("🎯 MyFuturePath MVP")

if st.session_state.learner_profile["name"] == "":
    name = st.text_input("What is your name?")

    if st.button("Start Learning") and name.strip():
        st.session_state.learner_profile["name"] = name
        st.session_state.lesson = determine_entry_point(st.session_state.learner_profile)
        st.rerun()

else:
    st.write(f"👋 Hello, **{st.session_state.learner_profile['name']}**!")

    # ---------------------------
    # LESSON FLOW
    # ---------------------------
    if st.session_state.lesson:
        # Show lesson
        st.markdown(deliver_lesson(st.session_state.lesson))

        # Current question
        question_data = get_next_question(st.session_state.practice_state, st.session_state.lesson)

        if question_data:
            st.subheader("📝 Practice Question")
            st.write(question_data["question"])

            # Show options as buttons
            selected_option = st.radio("Choose your answer:", question_data["options"], key=f"q_{st.session_state.practice_state['current_question']}")

            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("Submit Answer"):
                    feedback, status = handle_practice_attempt(
                        selected_option,
                        st.session_state.learner_profile,
                        st.session_state.practice_state,
                        st.session_state.lesson
                    )
                    st.info(feedback)

                    if status == "mastered":
                        st.session_state.show_next = True  # Allow student to control when to move on

                    elif status == "pause":
                        st.warning("Let's pause this topic and try another one later.")
                        st.session_state.learner_profile["history"][
                            st.session_state.learner_profile["current_topic"]
                        ] = "paused"
                        st.session_state.show_next = True

                    elif status == "retry":
                        st.warning("Try again. You can do it!")

            with col2:
                if st.button("Skip Topic"):
                    st.session_state.learner_profile["history"][
                        st.session_state.learner_profile["current_topic"]
                    ] = "skipped"
                    st.session_state.show_next = True

            # Move to next topic (student clicks manually)
            if st.session_state.show_next:
                if st.button("➡️ Next Topic"):
                    st.session_state.lesson = determine_entry_point(st.session_state.learner_profile)
                    st.session_state.practice_state = {"attempts": 0, "current_question": 0}
                    st.session_state.show_next = False
                    st.rerun()

        else:
            st.success("✅ You've completed all questions in this topic!")
            if st.button("➡️ Next Topic"):
                st.session_state.lesson = determine_entry_point(st.session_state.learner_profile)
                st.session_state.practice_state = {"attempts": 0, "current_question": 0}
                st.rerun()

    else:
        st.success("🎉 You have completed all available topics! Great job!")
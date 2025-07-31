import json
import random
from pathlib import Path

# ---------------------------
# LOAD LESSON DATA
# ---------------------------
LESSONS_PATH = Path("data/lessons.json")

with open(LESSONS_PATH, "r", encoding="utf-8") as f:
    lessons = json.load(f)

# ---------------------------
# DETERMINE ENTRY POINT
# ---------------------------
def determine_entry_point(profile):
    """Selects the next available topic from lessons.json based on learner history."""
    subjects = list(lessons.keys())
    random.shuffle(subjects)

    for subject in subjects:
        for topic, content in lessons[subject].items():
            if subject == "exposure":  # Skip exposure section
                continue
            status = profile["history"].get(topic, None)
            if status not in ["mastered", "paused", "skipped"]:
                profile["current_subject"] = subject
                profile["current_topic"] = topic
                return content
    return None

# ---------------------------
# DELIVER LESSON CONTENT
# ---------------------------
def deliver_lesson(lesson):
    """Formats lesson content into markdown."""
    output = f"## 📚 {lesson.get('meaning', 'No description')}\n\n"

    if "illustrations" in lesson and lesson["illustrations"]:
        output += "### ✏️ Examples:\n"
        for ex in lesson["illustrations"]:
            output += f"- {ex}\n"

    if "careers" in lesson and lesson["careers"]:
        output += "\n### 🌟 Career Connections:\n"
        for c in lesson["careers"]:
            output += f"- {c}\n"

    return output

# ---------------------------
# HANDLE PRACTICE ATTEMPTS
# ---------------------------
def handle_practice_attempt(selected_option, profile, practice_state, lesson):
    """Evaluates learner answers and decides on next step."""
    questions = lesson["practice"]
    current_index = practice_state["current_question"]

    if current_index >= len(questions):
        return "✅ You've finished all questions!", "mastered"

    correct_answer = questions[current_index]["answer"]

    if selected_option == correct_answer:
        practice_state["current_question"] += 1
        if practice_state["current_question"] >= len(questions):
            return "🎉 Correct! You've completed this topic!", "mastered"
        else:
            return "✅ Correct! Next question...", "mastered"
    else:
        practice_state["attempts"] += 1
        if practice_state["attempts"] < 3:
            return f"❌ Wrong! The correct answer was **{correct_answer}**. Try again!", "retry"
        else:
            return "😟 Too many wrong attempts. Let's pause this topic.", "pause"

# ---------------------------
# NEXT QUESTION HELPER
# ---------------------------
def get_next_question(practice_state, lesson):
    """Moves to the next question or ends topic."""
    if practice_state["current_question"] < len(lesson["practice"]):
        return lesson["practice"][practice_state["current_question"]]
    else:
        return None
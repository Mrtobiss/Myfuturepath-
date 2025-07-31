import json
from pathlib import Path

# ---------------------------
# PATHS
# ---------------------------
LESSONS_PATH = Path("data/lessons.json")

# ---------------------------
# CHECK LESSON FILE
# ---------------------------
def check_lessons():
    """Validate that lessons.json exists and can be read correctly."""
    if not LESSONS_PATH.exists():
        print(f"❌ lessons.json not found at {LESSONS_PATH}")
        return

    try:
        with open(LESSONS_PATH, "r", encoding="utf-8") as f:
            lessons = json.load(f)

        print("✅ lessons.json loaded successfully!\n")

        # Top-level sections
        print("Top-level sections:")
        for section in lessons.keys():
            print(f"  - {section}")

        # Print sample: first topic in math
        math_topics = lessons.get("math", {})
        if math_topics:
            first_topic = list(math_topics.keys())[0]
            print(f"\nSample topic from math: {first_topic}")
            print(f"Meaning: {math_topics[first_topic]['meaning']}")
        else:
            print("\n⚠️ No math topics found!")

    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    check_lessons()
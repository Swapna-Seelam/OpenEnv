def grade_easy(action, correct):
    return 1.0 if action == correct else 0.0


def grade_medium(action, correct):
    if action == correct:
        return 1.0
    elif action == "reply" and correct == "escalate":
        return 0.5
    return 0.0


def grade_hard(action, correct):
    if action == correct:
        return 1.0
    return 0.2  # harsh grading
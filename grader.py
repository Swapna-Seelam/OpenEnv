def grade_easy(env, action, obs):
    # env is an instance of EmailEnv
    if not hasattr(env, 'correct_action'):
        return 0.0
    return 1.0 if action.value == env.correct_action else 0.0

def grade_medium(env, action, obs):
    if not hasattr(env, 'correct_action'):
        return 0.0
    if action.value == env.correct_action:
        return 1.0
    elif action.value == "reply" and env.correct_action == "escalate":
        return 0.5
    return 0.0

def grade_hard(env, action, obs):
    if not hasattr(env, 'correct_action'):
        return 0.0
    if action.value == env.correct_action:
        return 1.0
    return 0.2
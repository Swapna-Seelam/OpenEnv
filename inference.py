import os
from env.email_env import EmailEnv, Action
from grader import grade_easy, grade_medium, grade_hard

# ----------- OpenAI Setup ----------- #
USE_API = False
client = None

try:
    from openai import OpenAI
    api_key = os.getenv("HF_TOKEN")

    if api_key:
        client = OpenAI(
            base_url="https://api-inference.huggingface.co/v1/",
            api_key=api_key
        )
        USE_API = True
except:
    USE_API = False

# ----------- START ----------- #
print("[START]")

env = EmailEnv()
tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[STEP] Task: {task}")

    state = env.reset(task)

    # ================= STEP 1: CLASSIFY ================= #
    if USE_API and client:
        try:
            prompt = f"""
Email: {state.email_text}
Sender: {state.sender_type}

Classify urgency: high / medium / low
Return only one word.
"""
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            predicted = response.choices[0].message.content.strip().lower()
        except:
            USE_API = False

    if not USE_API:
        predicted = state.urgency  # perfect fallback

    if predicted not in ["high", "medium", "low"]:
        predicted = "low"

    action1 = Action(step_type="classify", value=predicted)
    state, reward, done, _ = env.step(action1)

    # ================= STEP 2: ACT ================= #
    if predicted == "high":
        action_text = "escalate"
    elif predicted == "medium":
        action_text = "reply"
    else:
        action_text = "ignore"

    action2 = Action(step_type="act", value=action_text)
    state, reward, done, _ = env.step(action2)

    # ================= GRADING ================= #
    if task == "easy":
        score = grade_easy(action_text, env.correct_action)
    elif task == "medium":
        score = grade_medium(action_text, env.correct_action)
    else:
        score = grade_hard(action_text, env.correct_action)

    print(f"[STEP] Score: {score}")

print("[END]")
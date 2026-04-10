import os
import sys
from openai import OpenAI
from env import EmailEnv
from models import EmailAction

# Environment Variables with Defaults
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    print("Error: HF_TOKEN is required", file=sys.stderr)
    sys.exit(1)

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def run_task(task_id):
    env = EmailEnv()
    obs = env.reset(task_id=task_id)
    
    # [START] Exactly as required
    print(f"[START] task={task_id} env=email-triage-env model={MODEL_NAME}")
    
    rewards = []
    
    # Step 1: Classify
    prompt = f"Email: {obs.email_text}\nSender: {obs.sender_type}\nClassify urgency: high, medium, low. Return only one word."
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    predicted = resp.choices[0].message.content.strip().lower()
    
    action1 = EmailAction(step_type="classify", value=predicted)
    obs = env.step(action1) # Single object return
    rewards.append(obs.reward)
    
    # [STEP] Exactly as required
    print(f"[STEP] step=1 action=classify('{predicted}') reward={obs.reward:.2f} done={str(obs.done).lower()} error=null")
    
    # Step 2: Act
    if not obs.done:
        act_val = "reply" if predicted == "medium" else ("escalate" if predicted == "high" else "ignore")
        action2 = EmailAction(step_type="act", value=act_val)
        obs = env.step(action2)
        rewards.append(obs.reward)
        print(f"[STEP] step=2 action=act('{act_val}') reward={obs.reward:.2f} done={str(obs.done).lower()} error=null")

    # [END] Exactly as required
    success = sum(rewards) > 0.5
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={str(success).lower()} steps=2 rewards={rewards_str}")

if __name__ == "__main__":
    for t in ["task-easy", "task-medium", "task-hard"]:
        run_task(t)
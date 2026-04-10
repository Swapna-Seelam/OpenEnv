import os
import json
import sys
import traceback
from openai import OpenAI
from env.email_env import EmailEnv, EmailAction

# 1. Read environment variables with required defaults
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    # According to guidelines, HF_TOKEN is mandatory
    print("Error: HF_TOKEN environment variable is required", file=sys.stderr)
    sys.exit(1)

# 2. Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_task(task_name):
    env = EmailEnv()
    try:
        # [START] line
        print(f"[START] task={task_name} env=email-triage-env model={MODEL_NAME}")
        
        obs = env.reset(task_name=task_name)
        step_n = 1
        rewards = []
        done = False
        last_error = "null"

        # Step 1: Classify
        prompt = f"Email: {obs.email_text}\nSender: {obs.sender_type}\nClassify urgency as high, medium, or low. Return ONLY the word."
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            predicted_urgency = response.choices[0].message.content.strip().lower()
            if predicted_urgency not in ["high", "medium", "low"]:
                predicted_urgency = "low"
        except Exception as e:
            predicted_urgency = "low"
            last_error = str(e)

        # Execute Classification Step
        action_classify = EmailAction(step_type="classify", value=predicted_urgency)
        obs, reward, done, info = env.step(action_classify)
        rewards.append(reward)
        
        # [STEP] line
        print(f"[STEP] step={step_n} action=classify('{predicted_urgency}') reward={reward:.2f} done={str(done).lower()} error={last_error if last_error != 'null' else 'null'}")
        
        if not done:
            step_n += 1
            # Step 2: Act based on classification
            if predicted_urgency == "high":
                act_val = "escalate"
            elif predicted_urgency == "medium":
                act_val = "reply"
            else:
                act_val = "ignore"

            action_act = EmailAction(step_type="act", value=act_val)
            obs, reward, done, info = env.step(action_act)
            rewards.append(reward)
            
            # [STEP] line
            print(f"[STEP] step={step_n} action=act('{act_val}') reward={reward:.2f} done={str(done).lower()} error=null")

        # [END] line
        success = sum(rewards) > 0.5 # basic success metric
        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={str(success).lower()} steps={step_n} rewards={rewards_str}")

    except Exception as e:
        # Final [END] even on exception
        print(f"[END] success=false steps=0 rewards=0.00 error={str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    # Typically, the autograder runs inference for specific tasks
    # For a standalone run, we do a loop or just one
    for t in ["easy", "medium", "hard"]:
        run_task(t)
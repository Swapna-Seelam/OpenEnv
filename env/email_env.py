import random
import logging
from typing import Optional, Any
from openenv.core.env_server import Environment, Action, Observation

# ---------------- LOGGING ---------------- #
logger = logging.getLogger(__name__)

# ---------------- MODELS ---------------- #

class EmailObservation(Observation):
    email_text: str
    sender_type: str
    urgency: str


class EmailAction(Action):
    step_type: str   # "classify" or "act"
    value: str       # urgency OR action

# Aliases for backward compatibility
Action = EmailAction
Observation = EmailObservation

# ---------------- ENV ---------------- #

class EmailEnv(Environment):

    def __init__(self):
        super().__init__()
        self.current_email = None
        self.correct_action = None
        self.predicted_urgency = None
        self.steps = 0
        print("[DEBUG] EmailEnv initialized")

    # ----------- EMAIL GENERATION ----------- #
    def generate_email(self, difficulty):
        # Normalize difficulty
        difficulty = str(difficulty).lower()
        print(f"[DEBUG] Generating email for difficulty: {difficulty}")

        if "easy" in difficulty:
            emails = [
                ("Lunch plans?", "friend", "low", "ignore"),
                ("Meeting at 5 PM", "manager", "medium", "reply"),
            ]
        elif "medium" in difficulty:
            emails = [
                ("Reminder: submit weekly report", "manager", "medium", "reply"),
                ("Client issue: unable to login", "client", "high", "escalate"),
            ]
        else: # hard
            emails = [
                ("URGENT: Payment system failure affecting users", "client", "high", "escalate"),
                ("🔥 Congratulations! You won a free iPhone", "unknown", "low", "ignore"),
            ]

        self.current_email = random.choice(emails)
        self.correct_action = self.current_email[3]

    # ----------- RESET ----------- #
    def reset(self, task_name: str = "easy", **kwargs) -> EmailObservation:
        """
        Standard OpenEnv reset. 
        Note: task_name might be a string (from CLI) or an object (from autograder).
        """
        print(f"[DEBUG] Reset called with task_name={task_name} (type: {type(task_name)})")
        print(f"[DEBUG] kwargs received: {kwargs}")

        self.steps = 0
        self.predicted_urgency = None
        
        # Handle cases where task_name is actually a Task object
        name = "easy"
        if hasattr(task_name, 'name'):
            name = task_name.name
        elif isinstance(task_name, str):
            name = task_name
        
        if "easy" not in name and "medium" not in name and "hard" not in name:
            # Maybe it passed an ID like email-triage-easy
            if "easy" in name.lower(): name = "easy"
            elif "medium" in name.lower(): name = "medium"
            elif "hard" in name.lower(): name = "hard"

        self.generate_email(name)
        return self.state

    # ----------- STATE ----------- #
    @property
    def state(self) -> EmailObservation:
        if self.current_email is None:
             return EmailObservation(email_text="", sender_type="", urgency="")
        
        return EmailObservation(
            email_text=self.current_email[0],
            sender_type=self.current_email[1],
            urgency=self.current_email[2]
        )

    # ----------- STEP ----------- #
    def step(self, action: EmailAction):
        # Log action for debugging
        print(f"[DEBUG] Step called with action: {action}")

        self.steps += 1
        reward = 0.0
        done = False

        if self.steps >= 10:
            return self.state, -1.0, True, {"error": "Too many steps"}

        # -------- STEP 1: CLASSIFICATION -------- #
        if action.step_type == "classify":
            self.predicted_urgency = action.value
            if self.predicted_urgency == self.current_email[2]:
                reward += 0.5
            else:
                reward += 0.1

        # -------- STEP 2: FINAL ACTION -------- #
        elif action.step_type == "act":
            if action.value == self.correct_action:
                reward += 0.7
            else:
                reward += 0.2
            done = True

        # -------- PENALTY -------- #
        reward -= 0.05 * self.steps

        final_reward = round(float(reward), 2)
        print(f"[DEBUG] Step complete. Reward: {final_reward}, Done: {done}")
        return self.state, final_reward, done, {}
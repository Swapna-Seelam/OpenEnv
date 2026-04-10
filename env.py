import random
import time
from typing import Optional, Any
from openenv_core.env_server import Environment
from models import EmailAction, EmailObservation, EmailState

class EmailEnv(Environment):
    def __init__(self):
        self._state = EmailState()
        self.current_email = None

    @property
    def state(self) -> EmailState:
        return self._state

    def generate_email(self, difficulty: str):
        difficulty = difficulty.lower()
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
                ("URGENT: Payment system failure", "client", "high", "escalate"),
                ("Congratulations! won free iPhone", "unknown", "low", "ignore"),
            ]
        
        self.current_email = random.choice(emails)
        self._state.correct_action = self.current_email[3]
        print(f"[DEBUG] Generated email: {self.current_email[0]}")

    def reset(self, task_id: str = "task-easy", **kwargs) -> EmailObservation:
        self._state.task_id = task_id
        self._state.steps = 0
        self._state.predicted_urgency = None
        
        # Determine difficulty from task_id
        diff = "easy"
        if "medium" in task_id: diff = "medium"
        elif "hard" in task_id: diff = "hard"
        
        self.generate_email(diff)
        return self._get_obs(done=False, reward=0.0)

    def _get_obs(self, done: bool = False, reward: float = 0.0) -> EmailObservation:
        ts = time.strftime('%H:%M:%S')
        obs = EmailObservation(
            done=done,
            reward=reward,
            email_text=self.current_email[0] if self.current_email else "",
            sender_type=self.current_email[1] if self.current_email else "",
            urgency=self.current_email[2] if self.current_email else "",
            terminal_output=f"[{ts}] State: {self.current_email[0] if self.current_email else 'Initial'}"
        )
        return obs

    def step(self, action: EmailAction, **kwargs) -> EmailObservation:
        self._state.steps += 1
        reward = 0.0
        done = False
        
        if self._state.steps >= self._state.max_steps:
             return self._get_obs(done=True, reward=-1.0)

        # Logic
        if action.step_type == "classify":
            self._state.predicted_urgency = action.value
            reward = 0.4 if action.value == self.current_email[2] else 0.1
        elif action.step_type == "act":
            reward = 0.6 if action.value == self._state.correct_action else 0.1
            done = True
        
        return self._get_obs(done=done, reward=float(reward))

import random
from openenv.core.env_server import Environment, Action, Observation

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

    # ----------- EMAIL GENERATION ----------- #
    def generate_email(self, difficulty):

        if difficulty == "easy":
            emails = [
                ("Lunch plans?", "friend", "low", "ignore"),
                ("Meeting at 5 PM", "manager", "medium", "reply"),
            ]

        elif difficulty == "medium":
            emails = [
                ("Reminder: submit weekly report", "manager", "medium", "reply"),
                ("Client issue: unable to login", "client", "high", "escalate"),
            ]

        else:
            emails = [
                ("URGENT: Payment system failure affecting users", "client", "high", "escalate"),
                ("🔥 Congratulations! You won a free iPhone", "unknown", "low", "ignore"),
            ]

        self.current_email = random.choice(emails)
        self.correct_action = self.current_email[3]

    # ----------- RESET ----------- #
    def reset(self, task_name: str = "easy", **kwargs) -> EmailObservation:
        self.steps = 0
        self.predicted_urgency = None
        
        # OpenEnv autograders often pass 'task_name' or use the yaml names
        self.generate_email(task_name)

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

    # ----------- STEP (MULTI-STEP) ----------- #
    def step(self, action: EmailAction):
        self.steps += 1
        reward = 0.0
        done = False

        if self.steps >= 10:
            return self.state, -1.0, True, {"error": "Too many steps"}

        # -------- STEP 1: CLASSIFICATION -------- #
        if action.step_type == "classify":
            self.predicted_urgency = action.value

            if self.predicted_urgency == self.current_email[2]:
                reward += 0.5  # correct classification
            else:
                reward += 0.1  # partial credit

        # -------- STEP 2: FINAL ACTION -------- #
        elif action.step_type == "act":

            if action.value == self.correct_action:
                reward += 0.7
            else:
                reward += 0.2

            # bonus for correctly handling high urgency
            if self.current_email[2] == "high" and action.value == "escalate":
                reward += 0.3

            done = True  # task ends after action

        # -------- PENALTY -------- #
        reward -= 0.05 * self.steps

        return self.state, reward, done, {}
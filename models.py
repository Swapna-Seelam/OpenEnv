from typing import Literal, Optional
from pydantic import Field
from openenv_core.env_server import Action, Observation, State

class EmailAction(Action):
    step_type: Literal["classify", "act"] = Field(description="The type of action to take (classify or act)")
    value: str = Field(description="The urgency level OR the action string (reply/escalate/ignore)")

class EmailObservation(Observation):
    email_text: str = Field(default="", description="The content of the email")
    sender_type: str = Field(default="", description="The type of sender (friend/manager/client/unknown)")
    urgency: str = Field(default="", description="The urgency level (low/medium/high)")
    terminal_output: str = Field(default="", description="Status logs for the agent")

class EmailState(State):
    task_id: str = "task-easy"
    steps: int = 0
    max_steps: int = 10
    predicted_urgency: Optional[str] = None
    correct_action: Optional[str] = None

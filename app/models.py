from pydantic import BaseModel
from typing import List, Optional, Dict

# Define the chat message model
class ChatMessage(BaseModel):
    message: str
    thread_id: Optional[str] = None

# Define the message history model
class MessageHistory:
    def __init__(self):
        self.messages: List[dict] = []
        self.investment_profile: Dict = {
            "investment_goals": None,
            "monthly_investment": None,
            "risk_tolerance": None,
            "investment_horizon": None,
            "current_savings": None,
            "investment_experience": None,
            "target_passive_income": None
        }
        self.current_question: Optional[str] = None
        self.profile_complete: bool = False
        self.strategy_generated: bool = False 
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Define the chat message model
class ChatMessage(BaseModel):
    userId: str
    message: str
    thread_id: Optional[str] = None

# Define the message history model
class MessageHistory:
    def __init__(self):
        self.messages: List[dict] = []
        self.investment_profile: Dict[str, Dict[str, Any]] = {
            "personal_info": {
                "gender": None,
                "age": None,
                "marital_status": None,
                "expected_changes": None,
                "country": None
            },
            "investment_experience": {
                "experience": None,
                "stock_market_knowledge": None,
                "alternative_investments": None
            },
            "current_financial_status": {
                "monthly_income": None,
                "monthly_expenses": None,
                "monthly_savings": None,
                "total_savings": None,
                "savings_distribution": None,
                "financial_liabilities": None,
                "immediate_investment": None,
                "monthly_investment": None
            },
            "financial_security": {
                "emergency_fund": None,
                "months_coverage": None
            },
            "current_investments": {
                "existing_investments": None,
                "invested_percentage": None
            },
            "short_term_goals": {
                "goals": None,
                "amounts_needed": None,
                "timeline_flexibility": None
            },
            "mid_term_goals": {
                "goals": None,
                "amounts_needed": None,
                "timing_importance": None
            },
            "long_term_goals": {
                "goals": None,
                "retirement_amount": None,
                "target_age": None
            },
            "goal_prioritization": {
                "main_goals": None,
                "priority_ranking": None,
                "mandatory_goals": None
            },
            "risk_profile": {
                "profit_vs_preservation": None,
                "risk_tolerance": None,
                "decline_reaction": None,
                "acceptable_loss": None,
                "market_drop_reaction": None
            },
            "investment_preferences": {
                "investment_duration": None,
                "future_expenses": None,
                "liquidity_importance": None,
                "illiquid_assets": None
            },
            "restrictions": {
                "ethical_restrictions": None,
                "preferred_industries": None,
                "legal_restrictions": None,
                "personal_preferences": None
            },
            "investment_instruments": {
                "international_access": None,
                "available_instruments": None,
                "preferred_industries": None,
                "geographic_focus": None,
                "tax_efficiency": None
            },
            "success_metrics": {
                "success_definition": None,
                "return_expectations": None,
                "review_frequency": None,
                "life_events": None,
                "management_style": None
            }
        }
        self.current_category: Optional[str] = None
        self.current_question: Optional[str] = None
        self.profile_complete: bool = False
        self.strategy_generated: bool = False 
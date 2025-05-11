import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Investment advisor questions organized by categories
INVESTMENT_QUESTIONS: Dict[str, List[str]] = {
    "personal_info": [
        "What is your gender?",
        "How old are you?",
        "What is your marital status and number of dependents?",
        "Are there any expected changes in your marital/family status?",
        "What is your country of residence and tax residency?"
    ],
    
    "investment_experience": [
        "Do you have investment experience? If so, in which instruments?",
        "Have you previously invested in real estate or other alternative assets?"
    ],
    
    "current_financial_status": [
        "What is your current monthly income?",
        "What are your monthly expenses?",
        "How much do you currently save each month?",
        "Do you have financial liabilities (loans, mortgage, other debts)?",
        "How much are you willing to invest immediately?",
        "How much can you allocate monthly for investment?"
    ],
    
    "financial_security": [
        "Do you have an emergency fund for unforeseen situations?",
        "How many months of living expenses can your current savings cover without any income?"
    ],
    
    "current_investments": [
        "Do you already have any investments? If so, where?",
        "What percentage of your total capital is currently invested?"
    ],
    
    "short_term_goals": [
        "What specific financial goals do you want to achieve within the next 1–3 years?",
        "What is the approximate amount needed for each goal?",
        "How flexible are the timelines for achieving these goals?"
    ],
    
    "mid_term_goals": [
        "What financial goals do you plan to achieve within 3 to 10 years?",
        "What is the approximate amount needed for each of these goals?",
        "How important is the precise timing of these goals to you?"
    ],
    
    "goal_prioritization": [
        "What are your main financial goals? (e.g., retirement savings, home purchase, children's education, financial independence, passive income)",
        "Please rank these goals from 1 to 5 in order of priority",
        "Which goals are mandatory and which are desirable?"
    ],
    
    "risk_profile": [
        "What is more important: maximizing profit or preserving capital?",
        "What is your risk tolerance? (Conservative, Moderate, Aggressive)",
        "How do you react to temporary declines in investment value?",
        "What percentage loss is acceptable for you in the short term?",
        "How would you react to a temporary 20% drop in your investments' value?"
    ],
    
    "investment_preferences": [
        "For how long are you willing to invest funds without the need to withdraw them?",
        "Do you foresee any major expenses in the near future that may require using the invested funds?",
        "How important is the ability to quickly access invested funds to you?",
        "Are you willing to invest in less liquid assets for potentially higher returns?"
    ],
    
    "restrictions": [
        "Are there any industries or types of companies you would not want to invest in for ethical reasons?",
        "Are there industries or asset types that particularly interest or disinterest you?",
        "Are there legal or tax restrictions that may affect your investment decisions?",
        "Do you have personal preferences or ethical limitations regarding certain investments?"
    ],
    
    "investment_instruments": [
        "Do you have access to international capital markets?",
        "What investment instruments are available to you (brokerage accounts, retirement accounts, ETFs, cryptocurrencies, etc.)?",
        "Are you interested in particular industries or types of investments?",
        "Would you like to focus on specific geographic regions for investment?",
        "Are you interested in tax-efficient investments?"
    ],
    
    "success_metrics": [
        "How will you define the success of your investment strategy?",
        "What specific return metrics do you expect from your investments?",
        "How often do you plan to review and adjust your investment plan?",
        "What life events might prompt you to revisit your investment strategy?",
        "How actively do you want to manage your investments?"
    ]
}

# Store active threads
active_threads = {} 
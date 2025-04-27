from typing import Tuple, Optional
import re

def validate_response(category: str, question: str, response: str) -> Tuple[bool, Optional[str]]:
    """
    Validates the response based on category and question.
    Returns (is_valid, error_message).
    If is_valid is True, error_message is None.
    """
    
    # Convert response to lowercase for easier comparison
    response_lower = response.strip().lower()
    
    if not response_lower:
        return False, "Response cannot be empty."
        
    if category == "personal_info":
        if "gender" in question.lower():
            valid_genders = ["male", "female", "man", "woman", "other", "prefer not to say"]
            if not any(gender in response_lower for gender in valid_genders):
                return False, "Please specify your gender (male/female/other/prefer not to say)."
        
        elif "old" in question.lower() or "age" in question.lower():
            try:
                age = int(''.join(filter(str.isdigit, response)))
                if not (18 <= age <= 120):
                    return False, "Please provide a valid age between 18 and 120."
            except ValueError:
                return False, "Please provide your age as a number (18-120)."
        
        elif "marital status" in question.lower() and "changes" not in question.lower():
            valid_statuses = ["single", "married", "divorced", "widowed", "separated", "domestic partnership"]
            if not any(status in response_lower for status in valid_statuses):
                return False, "Please specify your marital status (single/married/divorced/widowed/separated/domestic partnership)."
        
        elif "changes" in question.lower():
            # First check if it's a yes/no response
            if any(answer in response_lower for answer in ["yes", "no"]):
                return True, None
            
            # Then check if it describes specific changes
            valid_changes = [
                "marriage", "wedding", "divorce", "child", "baby", 
                "adoption", "separation", "family", "partner", 
                "moving", "relocation"
            ]
            if not any(change in response_lower for change in valid_changes):
                return False, "Please specify if you expect any changes (yes/no) and if yes, what kind of changes (marriage, children, relocation, etc.)."
        
        elif "country" in question.lower():
            # Any non-empty response is valid for country
            return True, None
        
    elif category == "investment_experience":
        if "experience" in question.lower():
            if not any(level in response_lower for level in ["none", "beginner", "intermediate", "advanced", "expert"]):
                return False, "Please specify your experience level (none/beginner/intermediate/advanced/expert)."
                
    elif category == "current_financial_status":
        if any(keyword in question.lower() for keyword in ["monthly income", "monthly expenses", "save each month", "total amount"]):
            # Check if response contains a number with optional currency
            if not re.search(r'\d+', response):
                return False, "Please provide a numerical value."
            try:
                # Extract number from response
                amount = float(''.join(filter(str.isdigit, response)))
                if amount <= 0:
                    return False, "Please provide a positive number."
            except ValueError:
                return False, "Please provide a valid numerical amount."
                
    elif category == "financial_security":
        if "emergency fund" in question.lower():
            if not any(answer in response_lower for answer in ["yes", "no"]):
                return False, "Please answer with yes or no."
        elif "living expenses" in question.lower():
            try:
                months = float(''.join(filter(str.isdigit, response)))
                if months <= 0:
                    return False, "Please provide a positive number of months."
            except ValueError:
                return False, "Please specify the number of months."
                
    elif category == "risk_profile":
        if "risk tolerance" in question.lower():
            if not any(level in response_lower for level in ["low", "medium", "high", "conservative", "moderate", "aggressive"]):
                return False, "Please specify your risk tolerance level (low/medium/high or conservative/moderate/aggressive)."
        elif "loss" in question.lower() or "drop" in question.lower():
            try:
                percentage = float(''.join(filter(str.isdigit, response)))
                if not (0 <= percentage <= 100):
                    return False, "Please provide a valid percentage between 0 and 100."
            except ValueError:
                return False, "Please provide a valid percentage value."
                
    elif category == "investment_preferences":
        if "how long" in question.lower():
            if not any(timeframe in response_lower for timeframe in ["short", "medium", "long", "year", "month"]):
                return False, "Please specify a timeframe (short-term/medium-term/long-term or specific years/months)."
                
    elif category == "investment_instruments":
        if "international" in question.lower():
            if not any(answer in response_lower for answer in ["yes", "no", "limited"]):
                return False, "Please specify if you have access to international markets (yes/no/limited)."
                
    # If no specific validation rule was triggered, consider the response valid
    return True, None

def validate_response_coherence(category: str, question: str, response: str, previous_responses: dict) -> Tuple[bool, Optional[str]]:
    """
    Validates the coherence of the response with previous responses.
    Returns (is_coherent, error_message).
    """
    response_lower = response.strip().lower()
    
    if category == "current_financial_status":
        if "monthly savings" in question.lower() and "monthly_income" in previous_responses and "monthly_expenses" in previous_responses:
            try:
                income = float(''.join(filter(str.isdigit, previous_responses["monthly_income"])))
                expenses = float(''.join(filter(str.isdigit, previous_responses["monthly_expenses"])))
                savings = float(''.join(filter(str.isdigit, response)))
                
                if savings > income - expenses:
                    return False, "Monthly savings cannot be greater than income minus expenses."
            except ValueError:
                pass  # If we can't parse the numbers, skip this validation
                
    elif category == "investment_preferences":
        if "immediate investment" in question.lower() and "total_savings" in previous_responses:
            try:
                savings = float(''.join(filter(str.isdigit, previous_responses["total_savings"])))
                investment = float(''.join(filter(str.isdigit, response)))
                
                if investment > savings:
                    return False, "Immediate investment amount cannot be greater than total savings."
            except ValueError:
                pass
                
    elif category == "risk_profile":
        if "risk tolerance" in question.lower() and "age" in previous_responses:
            try:
                age = int(''.join(filter(str.isdigit, previous_responses["age"])))
                if age > 60 and "aggressive" in response_lower:
                    return False, "Consider if aggressive risk tolerance is appropriate for your age."
            except ValueError:
                pass
    
    return True, None 
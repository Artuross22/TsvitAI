from typing import List

# Function to extract investment goals from user response
def extract_investment_goals(response: str) -> List[str]:
    # Define possible investment goals
    possible_goals = [
        "retirement savings",
        "real estate purchase",
        "passive income generation",
        "children's education",
        "travel",
        "emergency fund",
        "other"
    ]
    
    # Check which goals are mentioned in the response
    found_goals = []
    for goal in possible_goals:
        if goal.lower() in response.lower():
            found_goals.append(goal)
    
    # If no goals found, return "other"
    if not found_goals:
        return ["other"]
    
    return found_goals 
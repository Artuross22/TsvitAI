import uuid
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models import ChatMessage, MessageHistory
from app.config import openai_api_key, active_threads, INVESTMENT_QUESTIONS
from app.services.strategy_service import generate_investment_strategy
from typing import Optional

def get_next_question(thread: MessageHistory) -> tuple[Optional[str], Optional[str]]:
    """Get the next question and category to ask."""
    if not thread.current_category:
        # Start with the first category
        next_category = list(INVESTMENT_QUESTIONS.keys())[0]
        return next_category, INVESTMENT_QUESTIONS[next_category][0]
    
    current_category = thread.current_category
    current_question = thread.current_question
    
    # Find current question index in current category
    current_questions = INVESTMENT_QUESTIONS[current_category]
    try:
        question_index = current_questions.index(current_question)
        
        # If there are more questions in current category
        if question_index < len(current_questions) - 1:
            return current_category, current_questions[question_index + 1]
        
        # Move to next category
        categories = list(INVESTMENT_QUESTIONS.keys())
        current_category_index = categories.index(current_category)
        
        # If there are more categories
        if current_category_index < len(categories) - 1:
            next_category = categories[current_category_index + 1]
            return next_category, INVESTMENT_QUESTIONS[next_category][0]
        
        # No more questions
        return None, None
        
    except ValueError:
        # Question not found in current category
        return None, None

def update_investment_profile(thread: MessageHistory, response: str) -> None:
    """Update the investment profile based on the current question and response."""
    if not thread.current_category or not thread.current_question:
        return
    
    category = thread.current_category
    question = thread.current_question
    profile = thread.investment_profile[category]
    
    # Map questions to profile fields based on category
    if category == "personal_info":
        if "gender" in question.lower():
            profile["gender"] = response
        elif "age" in question.lower():
            profile["age"] = response
        elif "marital status" in question.lower():
            profile["marital_status"] = response
        elif "changes" in question.lower():
            profile["expected_changes"] = response
        elif "country" in question.lower():
            profile["country"] = response
    
    elif category == "investment_experience":
        if "experience" in question.lower():
            profile["experience"] = response
        elif "stock market" in question.lower():
            profile["stock_market_knowledge"] = response
        elif "real estate" in question.lower():
            profile["alternative_investments"] = response
    
    elif category == "current_financial_status":
        if "monthly income" in question.lower():
            profile["monthly_income"] = response
        elif "monthly expenses" in question.lower():
            profile["monthly_expenses"] = response
        elif "save each month" in question.lower():
            profile["monthly_savings"] = response
        elif "total amount" in question.lower():
            profile["total_savings"] = response
        elif "distribution" in question.lower():
            profile["savings_distribution"] = response
        elif "liabilities" in question.lower():
            profile["financial_liabilities"] = response
        elif "invest immediately" in question.lower():
            profile["immediate_investment"] = response
        elif "allocate monthly" in question.lower():
            profile["monthly_investment"] = response
            
    elif category == "financial_security":
        if "emergency fund" in question.lower():
            profile["emergency_fund"] = response
        elif "living expenses" in question.lower():
            profile["months_coverage"] = response
            
    elif category == "current_investments":
        if "where" in question.lower():
            profile["existing_investments"] = response
        elif "percentage" in question.lower():
            profile["invested_percentage"] = response
            
    elif category == "short_term_goals":
        if "achieve within" in question.lower():
            profile["goals"] = response
        elif "amount needed" in question.lower():
            profile["amounts_needed"] = response
        elif "flexible" in question.lower():
            profile["timeline_flexibility"] = response
            
    elif category == "mid_term_goals":
        if "plan to achieve" in question.lower():
            profile["goals"] = response
        elif "amount needed" in question.lower():
            profile["amounts_needed"] = response
        elif "timing" in question.lower():
            profile["timing_importance"] = response
            
    elif category == "long_term_goals":
        if "financial goals" in question.lower():
            profile["goals"] = response
        elif "retirement" in question.lower():
            profile["retirement_amount"] = response
        elif "age" in question.lower():
            profile["target_age"] = response
            
    elif category == "goal_prioritization":
        if "main financial goals" in question.lower():
            profile["main_goals"] = response
        elif "rank" in question.lower():
            profile["priority_ranking"] = response
        elif "mandatory" in question.lower():
            profile["mandatory_goals"] = response
            
    elif category == "risk_profile":
        if "maximizing profit" in question.lower():
            profile["profit_vs_preservation"] = response
        elif "risk tolerance" in question.lower():
            profile["risk_tolerance"] = response
        elif "react to temporary" in question.lower():
            profile["decline_reaction"] = response
        elif "acceptable" in question.lower():
            profile["acceptable_loss"] = response
        elif "20% drop" in question.lower():
            profile["market_drop_reaction"] = response
            
    elif category == "investment_preferences":
        if "how long" in question.lower():
            profile["investment_duration"] = response
        elif "major expenses" in question.lower():
            profile["future_expenses"] = response
        elif "quickly access" in question.lower():
            profile["liquidity_importance"] = response
        elif "less liquid" in question.lower():
            profile["illiquid_assets"] = response
            
    elif category == "restrictions":
        if "ethical reasons" in question.lower():
            profile["ethical_restrictions"] = response
        elif "interest or disinterest" in question.lower():
            profile["preferred_industries"] = response
        elif "legal or tax restrictions" in question.lower():
            profile["legal_restrictions"] = response
        elif "personal preferences" in question.lower():
            profile["personal_preferences"] = response
            
    elif category == "investment_instruments":
        if "international capital markets" in question.lower():
            profile["international_access"] = response
        elif "instruments are available" in question.lower():
            profile["available_instruments"] = response
        elif "particular industries" in question.lower():
            profile["preferred_industries"] = response
        elif "geographic regions" in question.lower():
            profile["geographic_focus"] = response
        elif "tax-efficient" in question.lower():
            profile["tax_efficiency"] = response
            
    elif category == "success_metrics":
        if "define the success" in question.lower():
            profile["success_definition"] = response
        elif "return metrics" in question.lower():
            profile["return_expectations"] = response
        elif "review and adjust" in question.lower():
            profile["review_frequency"] = response
        elif "life events" in question.lower():
            profile["life_events"] = response
        elif "actively" in question.lower():
            profile["management_style"] = response
    
    thread.investment_profile[category] = profile

def process_chat(chat_message: ChatMessage):
    # Create or get thread
    if not chat_message.thread_id or chat_message.thread_id not in active_threads:
        thread_id = str(uuid.uuid4())
        active_threads[thread_id] = MessageHistory()
        # Start with first category and question
        next_category, next_question = get_next_question(active_threads[thread_id])
        active_threads[thread_id].current_category = next_category
        active_threads[thread_id].current_question = next_question
        
        # For new threads, return the first question directly
        return {
            "response": f"Hello! I'm your AI Investment Advisor. Let's develop your investment strategy. {next_question}",
            "thread_id": thread_id,
            "current_category": next_category,
            "current_question": next_question,
            "profile_complete": False
        }
    else:
        thread_id = chat_message.thread_id

    thread = active_threads[thread_id]
    
    # Update investment profile with user's response
    update_investment_profile(thread, chat_message.message)
    
    # Get next question
    next_category, next_question = get_next_question(thread)
    thread.current_category = next_category
    thread.current_question = next_question
    
    # Define the investment advisor prompt template
    chat_prompt = PromptTemplate(
        input_variables=["message", "history", "current_category", "current_question", "investment_profile"],
        template="""You are an experienced investment advisor AI assistant.
          Your role is to help users create an investment strategy based on their profile.

Current category: {current_category}
Current question being asked: {current_question}

User's investment profile so far:
{investment_profile}

Previous conversation:
{history}

If the user has answered the current question, analyze their response and provide appropriate feedback.
If the user hasn't answered the current question yet, guide them to answer it.
If all questions are answered, provide a detailed investment strategy recommendation based on their profile.

User: {message}
Assistant:"""
    )
    
    # Initialize OpenAI LLM
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    
    # Format conversation history
    history = "\n".join([
        f"User: {msg['user']}\nAssistant: {msg['assistant']}"
        for msg in thread.messages[-5:]
    ])
    
    # Format investment profile
    profile_str = "\n".join([
        f"{category}:\n" + "\n".join([f"  {k}: {v if v is not None else 'Not answered'}" 
                                     for k, v in profile.items()])
        for category, profile in thread.investment_profile.items()
    ])
    
    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    
    # Get response from AI
    response = chain.run(
        message=chat_message.message,
        history=history,
        current_category=thread.current_category,
        current_question=thread.current_question,
        investment_profile=profile_str
    )
    
    # Store the conversation
    thread.messages.append({
        "user": chat_message.message,
        "assistant": response
    })
    
    # Check if profile is complete
    if not next_category and not next_question:
        thread.profile_complete = True
    
    # Generate investment strategy if profile is complete and strategy hasn't been generated yet
    if thread.profile_complete and not thread.strategy_generated:
        strategy = generate_investment_strategy(thread)
        thread.strategy_generated = True
        return {
            "response": f"{response}\n\n{strategy}",
            "thread_id": thread_id,
            "current_category": thread.current_category,
            "current_question": thread.current_question,
            "profile_complete": thread.profile_complete,
            "strategy": strategy
        }
    
    # If there's a next question, append it to the response
    if next_question:
        response = f"{response}\n\n{next_question}"
    
    return {
        "response": response,
        "thread_id": thread_id,
        "current_category": thread.current_category,
        "current_question": thread.current_question,
        "profile_complete": thread.profile_complete
    }

def get_thread_history(thread_id: str):
    if thread_id not in active_threads:
        return {"error": "Thread not found"}
    
    thread = active_threads[thread_id]
    return {
        "messages": thread.messages,
        "investment_profile": thread.investment_profile,
        "current_category": thread.current_category,
        "current_question": thread.current_question,
        "profile_complete": thread.profile_complete
    } 
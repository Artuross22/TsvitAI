import uuid
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models import ChatMessage, MessageHistory
from app.config import openai_api_key, active_threads, INVESTMENT_QUESTIONS
from app.utils import extract_investment_goals
from app.services.strategy_service import generate_investment_strategy

def process_chat(chat_message: ChatMessage):
    # Create or get thread
    if not chat_message.thread_id or chat_message.thread_id not in active_threads:
        thread_id = str(uuid.uuid4())
        active_threads[thread_id] = MessageHistory()
        # Start with first question
        current_question = INVESTMENT_QUESTIONS[0]
        active_threads[thread_id].current_question = current_question
        
        # For new threads, return the first question directly
        return {
            "response": f"Hello! I'm your AI Investment Advisor. Let's develop your investment strategy. {current_question}",
            "thread_id": thread_id,
            "current_question": current_question,
            "profile_complete": False
        }
    else:
        thread_id = chat_message.thread_id

    thread = active_threads[thread_id]
    
    # Define the investment advisor prompt template
    chat_prompt = PromptTemplate(
        input_variables=["message", "history", "current_question", "investment_profile"],
        template="""You are an experienced investment advisor AI assistant.
          Your role is to help users create an investment strategy based on their profile.

Current question being asked: {current_question}

User's investment profile so far:
{investment_profile}

Previous conversation:
{history}

If the user has answered the current question, analyze their response and update the investment profile accordingly.
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
        f"{key}: {value if value is not None else 'Not answered'}"
        for key, value in thread.investment_profile.items()
    ])
    
    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    
    # Get response from AI
    response = chain.run(
        message=chat_message.message,
        history=history,
        current_question=thread.current_question,
        investment_profile=profile_str
    )
    
    # Store the conversation
    thread.messages.append({
        "user": chat_message.message,
        "assistant": response
    })
    
    # Update investment profile based on the current question
    if not thread.profile_complete:
        current_question_index = INVESTMENT_QUESTIONS.index(thread.current_question)
        
        # Extract information based on the current question
        if current_question_index == 0:  # Investment goals
            thread.investment_profile["investment_goals"] = extract_investment_goals(chat_message.message)
        elif current_question_index == 1:  # Investment horizon
            thread.investment_profile["investment_horizon"] = chat_message.message
        elif current_question_index == 2:  # Monthly investment
            thread.investment_profile["monthly_investment"] = chat_message.message
        elif current_question_index == 3:  # Investment experience
            thread.investment_profile["investment_experience"] = chat_message.message
        elif current_question_index == 4:  # Risk tolerance
            thread.investment_profile["risk_tolerance"] = chat_message.message
        elif current_question_index == 5:  # Current savings
            thread.investment_profile["current_savings"] = chat_message.message
        elif current_question_index == 6:  # Target amount of passive income
            thread.investment_profile["target_passive_income"] = chat_message.message

        
        # Move to next question
        if current_question_index < len(INVESTMENT_QUESTIONS) - 1:
            thread.current_question = INVESTMENT_QUESTIONS[current_question_index + 1]
        else:
            thread.profile_complete = True
    
    # Generate investment strategy if profile is complete and strategy hasn't been generated yet
    if thread.profile_complete and not thread.strategy_generated:
        strategy = generate_investment_strategy(thread)
        thread.strategy_generated = True
        return {
            "response": f"{response}\n\n{strategy}",
            "thread_id": thread_id,
            "current_question": thread.current_question,
            "profile_complete": thread.profile_complete,
            "strategy": strategy
        }
    
    return {
        "response": response,
        "thread_id": thread_id,
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
        "current_question": thread.current_question,
        "profile_complete": thread.profile_complete
    } 
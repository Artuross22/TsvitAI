from fastapi import FastAPI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

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
            "investment_experience": None
        }
        self.current_question: Optional[str] = None
        self.profile_complete: bool = False
        self.strategy_generated: bool = False

# Store active threads
active_threads = {}

# Investment advisor questions
INVESTMENT_QUESTIONS = [
    "What are your financial goals? (Choose one or more options: retirement savings, real estate purchase, passive income generation, children's education, travel, emergency fund, other)",
    "What is your time horizon for achieving these goals? (short-term - up to 1 year, medium-term - 1-5 years, long-term - more than 5 years)",
    "How much can you invest monthly?",
    "What is your level of investment experience? (beginner, intermediate, experienced)",
    "What is your risk tolerance? (low, medium, high)",
    "What are your current savings available for investment?"
]

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

# Function to generate investment strategy
def generate_investment_strategy(thread: MessageHistory):
    # Define the strategy generation prompt template
    strategy_prompt = PromptTemplate(
        input_variables=["investment_profile"],
        template="""You are an experienced investment advisor AI assistant.
        Based on the user's investment profile, create a detailed investment strategy.
        
        User's investment profile:
        {investment_profile}
        
        Provide a comprehensive investment strategy that includes:
        1. Asset allocation recommendations (stocks, bonds, real estate, etc.)
        2. Specific investment vehicles or funds to consider
        3. Risk management strategies
        4. Timeline for reviewing and adjusting the strategy
        5. Additional recommendations based on their profile
        
        Investment Strategy:"""
    )
    
    # Initialize OpenAI LLM
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    
    # Format investment profile
    profile_str = "\n".join([
        f"{key}: {value if value is not None else 'Not answered'}"
        for key, value in thread.investment_profile.items()
    ])
    
    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=strategy_prompt)
    
    # Get strategy from AI
    strategy = chain.run(investment_profile=profile_str)
    
    return strategy

# Chat endpoint
@app.post("/chat")
def chat(chat_message: ChatMessage):
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

# Get thread history endpoint
@app.get("/thread/{thread_id}")
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
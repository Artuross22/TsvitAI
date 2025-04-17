from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models import MessageHistory
from app.config import openai_api_key

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
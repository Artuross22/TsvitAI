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
        Based on the user's comprehensive investment profile, create a detailed investment strategy.
        
        User's investment profile:
        {investment_profile}
        
        Please provide a comprehensive investment strategy that includes:
        
        1. Executive Summary
        - Brief overview of the client's profile
        - Key financial goals and priorities
        - Overall risk tolerance assessment
        
        2. Asset Allocation Strategy
        - Recommended portfolio allocation across different asset classes
        - Specific allocation percentages based on risk profile
        - Geographic diversification strategy
        
        3. Investment Vehicle Recommendations
        - Specific investment products and vehicles
        - Tax-efficient investment options
        - Consideration of ESG preferences
        
        4. Risk Management Strategy
        - Diversification approach
        - Hedging strategies if applicable
        - Emergency fund recommendations
        
        5. Implementation Timeline
        - Phased investment approach
        - Rebalancing schedule
        - Major milestones and checkpoints
        
        6. Monitoring and Review Plan
        - Performance metrics and benchmarks
        - Review frequency and triggers
        - Adjustment criteria
        
        7. Additional Considerations
        - Tax optimization strategies
        - Estate planning considerations
        - Insurance recommendations if applicable
        
        Please provide specific, actionable recommendations while considering the client's unique circumstances, constraints, and preferences.
        
        Investment Strategy:"""
    )
    
    # Initialize OpenAI LLM
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    
    # Format investment profile with detailed categorization
    profile_sections = []
    for category, profile in thread.investment_profile.items():
        section = f"\n{category.replace('_', ' ').title()}:\n"
        for key, value in profile.items():
            formatted_key = key.replace('_', ' ').title()
            section += f"  {formatted_key}: {value if value is not None else 'Not provided'}\n"
        profile_sections.append(section)
    
    profile_str = "\n".join(profile_sections)
    
    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=strategy_prompt)
    
    # Get strategy from AI
    strategy = chain.run(investment_profile=profile_str)
    
    return strategy 
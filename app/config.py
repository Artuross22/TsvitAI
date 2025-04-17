import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Investment advisor questions
INVESTMENT_QUESTIONS = [
    "What are your financial goals? (Choose one or more options: retirement savings, real estate purchase, passive income generation, children's education, travel, emergency fund, other)",
    "What is your time horizon for achieving these goals? (short-term - up to 1 year, medium-term - 1-5 years, long-term - more than 5 years)",
    "How much can you invest monthly?",
    "What is your level of investment experience? (beginner, intermediate, experienced)",
    "What is your risk tolerance? (low, medium, high)",
    "What are your current savings available for investment?",
    "What is your target amount of passive income per month?"
]

# Store active threads
active_threads = {} 
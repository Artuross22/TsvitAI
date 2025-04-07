from fastapi import FastAPI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Головна сторінка
@app.get("/")
def read_root():
    return {"message": "Привіт, FastAPI!"}

# Динамічний маршрут
@app.get("/hello/{name}")
def read_item(name: str):

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Q: {question}\nA:"
    )
    
    # Initialize OpenAI LLM
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

    # Create a chain with the LLM and prompt
    chain = LLMChain(llm=llm, prompt=prompt)

    # Ask a question
    question = f"What is the capital of {name}?"
    response = chain.run(question)
    print(response)
   
    return {"message": f"Привіт, {response}!"}
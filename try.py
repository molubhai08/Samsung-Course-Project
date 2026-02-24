
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Define system prompt
system_prompt = """
You are a helpful AI assistant.

Instructions:
- Be clear and concise
- Answer step-by-step when needed
- If you don't know the answer, say you don't know
- Avoid assumptions
- Keep responses professional
"""

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

# Create messages
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="Explain LangChain in simple terms")
]

# Run model
response = llm.invoke(messages)

# Output
print(response.content)
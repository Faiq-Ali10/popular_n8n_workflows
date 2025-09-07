from typing import List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from prompt import prompt
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("GEMNI_API_KEY")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash-lite",
    api_key=SecretStr(api) if api else None
)

def llm_response(values: List[Tuple]) -> str:
    # Send a single prompt
    question = prompt(values)
    print(question)
    response = llm.invoke(question)
    print("LLM\n")
    print(response.content)
    print("LLM\n")

    if hasattr(response, "content") and isinstance(response.content, str):
        return response.content.strip()

    # If response is just a string
    if isinstance(response, str):
        return response.strip()

    # Fallback
    return str(response).strip()
    
def helper(workflows):
    print(workflows)
    result = []
    workflows_names = []
    for idx, wf in enumerate(workflows):
        workflows_names.append((idx, wf.workflow))
        
    response = llm_response(workflows_names)
    valid_workflows_idxs = [int(x.strip()) for x in response.split(",") if x.strip().isdigit()]
    
    for i in range(len(workflows)):
        if(i in valid_workflows_idxs):
            result.append(workflows[i])
            
    return result   

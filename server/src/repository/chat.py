from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.schemas.chat import Response
from src.services.llmchain import Chain
API_KEY = "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"

chain = Chain()

def respond(instruction: str) -> str:
    response = chain(instruction).lstrip()
    return Response(string=response)
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.schemas.chat import Response
API_KEY = "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"

llm = HuggingFaceHub(repo_id="databricks/dolly-v2-3b", huggingfacehub_api_token = API_KEY)
prompt = PromptTemplate(
    input_variables=["instruction"],
    template="{instruction}")
llm_chain = LLMChain(llm=llm, prompt=prompt)

def respond(instruction: str) -> str:
    response = llm_chain.predict(instruction=instruction).lstrip()
    return Response(string=response)
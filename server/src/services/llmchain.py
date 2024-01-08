from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

from ..config.settings import settings
from ..config.llm_list import LLMNameEnum
from ..vector_db.chroma_init import get_chroma_client
from ..repository.history import extract_history, get_selected_llm
from pprint import pprint

API_KEY = settings.llm_api_key


#llm_id = "databricks/dolly-v2-3b"
#llm_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

transformer_id = "sentence-transformers/all-MiniLM-L6-v2"

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible.
{context}
If the context is empty you can propose the user to upload their documents.
Chat history:
{chat_history}
Question: {question}
Helpful Answer:"""


prompt = PromptTemplate.from_template(template)

template_no_context = """Answer the question at the end. Use three sentences maximum. Keep the answer as concise as possible.
{chat_history}
Question: {input}
Helpful Answer:"""

prompt_no_context = PromptTemplate.from_template(template_no_context)


class Chain:
    def __init__(self, history=[]):
        self.llm = {}
        for llm_id in LLMNameEnum:
            self.llm[llm_id.value] = HuggingFaceHub(
                repo_id=llm_id.value,
                huggingfacehub_api_token=API_KEY,
                model_kwargs={"temperature": 0.2, "max_length": 255},
            )
        self.chains = {}
        self.embedding_function = SentenceTransformerEmbeddings(model_name=transformer_id)


    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    

    def create_context(self, user_id):
        client = get_chroma_client()
        client.get_or_create_collection(f"collection_{user_id}") #creates empty collection if it does't exist
        context = Chroma(
                    client=client,
                    collection_name=f"collection_{user_id}",
                    embedding_function=self.embedding_function,)
        return context
            

    async def create_memory(self, user_id):
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        history = await extract_history(user_id)
        for i in history:
            memory.save_context({"input": i[0]}, {"output": i[1]})

        return memory
    
    async def get_llm(self, user_id):
        llm_id = await get_selected_llm(user_id)
        llm = self.llm[llm_id]
        return llm

    async def create_chain(self, user_id):
        context = self.create_context(user_id)
        llm = await self.get_llm(user_id)
        memory = await self.create_memory(user_id)
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            context.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": prompt}
        )
        return chain

    def answer(self, query, user_id):
        result = self.chains[user_id]({"question": query})
        return result["answer"].lstrip()
        
    
    async def update(self, user_id):
        self.chains[user_id] = await self.create_chain(user_id)

    
    def delete_chain(self, user_id):
        self.chains.pop(user_id)
        

    async def __call__(self, query, user_id):
        if user_id not in self.chains.keys():
            self.chains[user_id] = await self.create_chain(user_id)
        return self.answer(query, user_id)

chain = Chain()
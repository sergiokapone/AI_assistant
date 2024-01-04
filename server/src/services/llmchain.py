from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..config.settings import settings

API_KEY = settings.llm_api_key

llm_id = "databricks/dolly-v2-3b"
llm_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

transformer_id = "sentence-transformers/all-MiniLM-L6-v2"

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible.
{context}
Question: {question}
Helpful Answer:"""


prompt = PromptTemplate.from_template(template)

template_no_context = """Your name is AIS{user_id}. Answer the question at the end. Use three sentences maximum. Keep the answer as concise as possible.
Question: {question}
Helpful Answer:"""

prompt_no_context = PromptTemplate.from_template(template_no_context)


class Chain:
    def __init__(self, context=None, history=[]):
        self.llm = HuggingFaceHub(
            repo_id=llm_id,
            huggingfacehub_api_token=API_KEY,
            model_kwargs={"temperature": 0.2, "max_length": 255},
        )
        self.context = context
        self.hostory = history  # NYI
        if context:
            self.retriever = context.as_retriever()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def create_chain(self):
        if self.context:
            self.chain = (
                {
                    "context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )
        else:
            self.chain = (
                {
                    "user_id": self.get_current_user,
                    "question": RunnablePassthrough(),
                }
                | prompt_no_context
                | self.llm
                | StrOutputParser()
            )

    def get_current_user(self, *args):
        return str(self.current_user)

    def create_context(self):
        # Тут создается vectorstore self.context и retriever

        self.create_chain()  # после создания контекста создается новая сеть, которая будет работать с ним.

    def add_context(self):
        pass  # Когда мы найдем способ добавлять новые документы в контекст он будет имплиментирован здесь.

    def __call__(self, query, user_id):
        self.current_user = user_id
        self.create_chain()
        return self.chain.invoke(query)

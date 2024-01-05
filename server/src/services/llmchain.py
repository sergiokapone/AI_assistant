from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

from ..config.settings import settings
from ..vector_db.chroma_init import get_chroma_client

API_KEY = settings.llm_api_key


# llm_id = "databricks/dolly-v2-3b"
llm_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

transformer_id = "sentence-transformers/all-MiniLM-L6-v2"

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible.
{context}
Question: {question}
Helpful Answer:"""


prompt = PromptTemplate.from_template(template)

template_no_context = """Answer the question at the end. Use three sentences maximum. Keep the answer as concise as possible.
Question: {question}
Helpful Answer:"""

prompt_no_context = PromptTemplate.from_template(template_no_context)


class Chain:
    def __init__(self, history=[]):
        self.llm = HuggingFaceHub(
            repo_id=llm_id,
            huggingfacehub_api_token=API_KEY,
            model_kwargs={"temperature": 0.2, "max_length": 255},
        )
        self.context = None
        self.hostory = history  # NYI
        self.embedding_function = SentenceTransformerEmbeddings(model_name=transformer_id)

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def create_chain(self):
        if self.context:
            self.chain = (
                {
                    "context": self.context.as_retriever() | self.format_docs,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )
        else:
            self.chain = (
                {"question": RunnablePassthrough(),}
                | prompt_no_context
                | self.llm
                | StrOutputParser()
            )

    def create_context(self, user_id):
        client = get_chroma_client()
        try:
            tmp_collection = client.get_collection(f"collection_{user_id}") #raises ValueError if the collection does't exist
            self.context = Chroma(
                        client=client, #will be imported from "extract_text_from_pdf"
                        collection_name=f"collection_{user_id}",
                        embedding_function=self.embedding_function,)
        except ValueError:
            self.context = None

    def __call__(self, query, user_id):
        self.create_context(user_id)
        self.create_chain()
        return self.chain.invoke(query)

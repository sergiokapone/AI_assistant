# import
from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# load the document and split it into chunk
loader = TextLoader("output.txt", encoding='utf-8')
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# load it into Chroma and save to disk
db = Chroma.from_documents(docs, embedding_function, persist_directory="chroma_db")
transformer_id = "sentence-transformers/all-MiniLM-L6-v2"
retriever = db.as_retriever()


print("ready")

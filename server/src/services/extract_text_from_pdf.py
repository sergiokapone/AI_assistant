import os
import tempfile
import PyPDF2
import re
import uuid

from typing import Union, List

import chromadb
from chromadb.config import Settings

# import
from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


# read only digital PDF book which more 1000 sings
def extract_text_from_pdf(pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]]):
    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""

        for page in reader.pages:
            _pdf_text += page.extract_text()
        # Очищаем текст от недопустимых символов и тегов
        cleaned_text_pdf = re.sub(r'[\d/.]', '', _pdf_text)
        # print(f"text in the var: {cleaned_text}")

        # Try Chroma Client
        # chroma_client = chromadb.Client()
        chroma_client = chromadb.PersistentClient(path="chromadb", settings=Settings(allow_reset=True))
        print(chroma_client.heartbeat())

        # metadata_options = {"hnsw:space": "cosine"}  # You can change this to "ip" or "cosine" if needed
        new_collection_persistent = chroma_client.create_collection(name="collection_name_persistent",
                                                                    metadata={"hnsw:space": "cosine"})
        # This allows us to create a client that connects to the server
        # collection = chroma_client.create_collection(name="cleaned_text_pdf", metadata=metadata_options)
        print(new_collection_persistent)

        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_text(cleaned_text_pdf)
        print(docs)
        for doc in docs:
            uuid_name = uuid.uuid1()
            print("document for", uuid_name)
            new_collection_persistent.add(ids=[str(uuid_name)], documents=doc)
        print(new_collection_persistent)


# C:/Users/User/Downloads/design-patterns-uk.pdf
def get_to_pdf():
    # Спрашиваем у пользователя, сколько файлов он хотел бы загрузить
    num_files = int(input("How many PDF files would you like to upload? - "))
    pdf_paths = []
    # Просим пользователя ввести путь к каждому файлу
    for i in range(num_files):
        while True:
            pdf_path = input(f"Please enter full path to PDF #{i + 1}: ")
            # Проверяем, является ли указанный путь файлом PDF
            if not pdf_path.lower().endswith(".pdf"):
                print("!!! Specified file is not a PDF file.")
                continue
            # Проверяем, существует ли указанный файл
            if not os.path.isfile(pdf_path):
                print("!!! The specified file does not exist.")
                continue
            break
        pdf_paths.append(pdf_path)

    # Вызываем функцию extract_text_from_pdf с указанными путями к PDF-файлам
    extract_text_from_pdf(pdf_paths)


if __name__ == "__main__":
    get_to_pdf()

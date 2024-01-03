import os
import tempfile
import PyPDF2
import re
import uuid
import chromadb

from typing import Union, List
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from server.src.database.models import User

# Глобальные переменные
chroma_client = None
collection_name = None
new_collection_persistent = None


# Инициализация Chroma Client и создание коллекции
def initialize_chroma_client(user_id, text_from_pdf):
    global chroma_client, collection_name, new_collection_persistent

    # Создаем Chroma Client, если он не был создан ранее
    if chroma_client is None:
        chroma_client = chromadb.PersistentClient(path="../../chromadb", settings=Settings(allow_reset=True))
        print(chroma_client.heartbeat())

    collection_name = f"collection_{user_id}"
    new_collection_persistent = chroma_client.get_or_create_collection(name=collection_name,
                                                                       metadata={"hnsw:space": "cosine"})
    print(new_collection_persistent)

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_text(text_from_pdf)

    for doc in docs:
        uuid_name = uuid.uuid1()
        print("document for", uuid_name)
        new_collection_persistent.add(ids=[str(uuid_name)], documents=doc)


# read only digital PDF book which more 1000 sings
def extract_text_from_pdf(pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]], user_id):
    global collection_name
    cleaned_text_pdf = ""

    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""

        for page in reader.pages:
            _pdf_text += page.extract_text()
        # Очищаем текст от недопустимых символов и тегов
        cleaned_text_pdf = re.sub(r'[\d/.]', '', _pdf_text)

    initialize_chroma_client(user_id, cleaned_text_pdf)


# C:/Users/User/Downloads/cannon-2023-predicting-conversion-to-psychosis-using-machine-learning-are-we-there-yet.pdf
# C:/Users/User/Downloads/design-patterns-uk.pdf
# def get_to_pdf():
# Спрашиваем у пользователя, сколько файлов он хотел бы загрузить
# num_files = int(input("How many PDF files would you like to upload? - "))
# pdf_paths = []
# Просим пользователя ввести путь к каждому файлу
# for i in range(num_files):
#     while True:
#         pdf_path = input(f"Please enter full path to PDF #{i + 1}: ")
# Проверяем, является ли указанный путь файлом PDF
# if not pdf_path.lower().endswith(".pdf"):
#     print("!!! Specified file is not a PDF file.")
#     continue
# Проверяем, существует ли указанный файл
#     if not os.path.isfile(pdf_path):
#         print("!!! The specified file does not exist.")
#         continue
#     break
# pdf_paths.append(pdf_path)

# Вызываем функцию extract_text_from_pdf с указанными путями к PDF-файлам
# cleaned_text_pdf = extract_text_from_pdf(pdf_paths)

# Вызываем функцию инициализации Chroma Client с очищенным текстом
# initialize_chroma_client(cleaned_text_pdf)


if __name__ == "__main__":
    # get_to_pdf()
    # Здесь мы можем получить id пользователя из веб-приложения или другого источника данных
    user_id = "12345"  # Здесь нужно использовать реальный id пользователя
    pdf_paths = ["path/to/pdf1.pdf", "path/to/pdf2.pdf"]  # Здесь нужно указать реальные пути к PDF-файлам

    extract_text_from_pdf(pdf_paths, user_id)


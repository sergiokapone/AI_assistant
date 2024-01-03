import re
import tempfile
import uuid
from typing import List, Union

import chromadb
import PyPDF2
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..database.models import User

# Глобальные переменные
chroma_client = None
# collection_name = None
# new_collection_persistent = None


# Инициализация Chroma Client и создание коллекции
def initialize_chroma_client():
    global chroma_client

    # Создаем Chroma Client, если он не был создан ранее
    if chroma_client is None:
        chroma_client = chromadb.PersistentClient(
            path="../../chromadb", settings=Settings(allow_reset=True)
        )
        print(chroma_client.heartbeat())


# read only digital PDF book which more 1000 sings


def extract_text_from_pdf(
    current_user: User,
    pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]],
) -> None:
    global collection_name
    cleaned_text_pdf = ""

    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""

        for page in reader.pages:
            _pdf_text += page.extract_text()
        # Очищаем текст от недопустимых символов и тегов

        cleaned_text_pdf = re.sub(r"[\d/.]", "", _pdf_text)

    collection_name = f"collection_{current_user.id}"
    new_collection_persistent = chroma_client.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )

    print(new_collection_persistent)

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=20
    )
    docs = text_splitter.split_text(cleaned_text_pdf)

    for doc in docs:
        uuid_name = uuid.uuid1()
        print("document for", uuid_name)
        new_collection_persistent.add(ids=[str(uuid_name)], documents=doc)


if __name__ == "__main__":
    # get_to_pdf()
    # Здесь мы можем получить id пользователя из веб-приложения или другого источника данных
    user_id = "12345"  # Здесь нужно использовать реальный id пользователя
    pdf_paths = [
        "C:/Users/User/Downloads/cannon-2023-predicting-conversion-to-psychosis-using-machine-learning-are-we-there-yet.pdf",
        "C:/Users/User/Downloads/design-patterns-uk.pdf",
    ]  # Здесь нужно указать реальные пути к PDF-файлам

    extract_text_from_pdf(pdf_paths, user_id)

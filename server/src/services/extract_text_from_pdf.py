import os
import tempfile
import chromadb
import PyPDF2

from typing import Union, List

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import LlamaCppEmbeddings

chroma = Chroma()
# Chunking the text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


# read only digital PDF book which more 1000 sings
def extract_text_from_pdf(pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]]):
    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""
        # page_number = 0

        for page in reader.pages:
            # page_number += 1
            _pdf_text += page.extract_text()
            # _pdf_text += page.extract_text() + f"\nPage Number: {page_number}"
        print(type(_pdf_text))

        # Разбиваем текст на части
        text_parts = text_splitter.split_text(_pdf_text)

        # create the open-source embedding function
        embedding_function = LlamaCppEmbeddings(
            model_path="D:\PYTHON\DataScience\AI_assistant\server\src\model\llama-2-7b-chat.Q4_K_S.gguf")
        docsearch = chroma.from_texts(text_parts, embedding_function)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            chain_type="stuff",
            retriever=docsearch.as_retriever(),
        )
        print(chain)

        # load it into Chroma
        db = chroma.from_documents(text_parts, embedding_function)
        print(db)

        # query it
        query = "інкапсулювати щось всередині класу"
        text_parts = db.similarity_search(query)

        # Отправляем каждую часть в базу данных Chroma
        # for i, part in enumerate(text_parts):
        #     chroma.store_vector(f"pdf_part_{i}", part)
        # print("The text of the PDF file has been successfully broken down and transferred to the Chroma database.")

        print(text_parts)


if __name__ == "__main__":
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

import os
import tempfile
import chromadb
import PyPDF2

from typing import Union, List
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

chroma = Chroma()
# Chunking the text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


def extract_text_from_pdf(pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]]):
    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""
        page_number = 0

        for page in reader.pages:
            page_number += 1
            _pdf_text += page.extract_text() + f"\nPage Number: {page_number}"

        # Разбиваем текст на части
        text_parts = text_splitter.split_text(_pdf_text)

        db = chroma.from_documents(text_parts)
        # Отправляем каждую часть в базу данных Chroma
        for i, part in enumerate(text_parts):
            chroma.store_vector(f"pdf_part_{i}", part)
        print("The text of the PDF file has been successfully broken down and transferred to the Chroma database.")

        print(text_parts[0].page_content)


if __name__ == "__main__":
    while True:
        # example_path = "D:\PYTHON\DataScience\TP_DS_23_tg1\AI_assistant\server\src\services\design-patterns-uk.pdf"
        pdf_path = input("Please enter path to PDF: ")
        if not pdf_path.lower().endswith(".pdf"):
            print("Specified file is not a file PDF.")
            continue

        if not os.path.isfile(pdf_path):
            print("The specified file does not exist.")
            continue
       
        extract_text_from_pdf([pdf_path])
        break



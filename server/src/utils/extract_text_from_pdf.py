import tempfile
from typing import Union
import chromadb
import PyPDF2

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

chroma = Chroma()
# Chunking the text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


# reader = PyPDF2.PdfReader("report_07-12-23_17-58-01.pdf")
# page = reader.pages[0]
# print(page.extract_text())


def extract_text_from_pdf(pdf_source):
    # Читаем PDF файл
    reader = PyPDF2.PdfReader(pdf_source)
    _pdf_text = ""
    page_number = 0

    for page in reader.pages:
        page_number += 1
        _pdf_text += page.extract_text() + f"\nPage Number: {page_number}"

    # Разбиваем текст на части
    text_parts = text_splitter.split_text(_pdf_text)

    # db = chroma.from_documents(text_parts)
    # Отправляем каждую часть в базу данных Chroma
    # for i, part in enumerate(text_parts):
    #     chroma.store_vector(f"pdf_part_{i}", part)
    # print("The text of the PDF file has been successfully broken down and transferred to the Chroma database.")

    # print(text_parts[0].page_content)


if __name__ == "__main__":
    extract_text_from_pdf("design-patterns-uk.pdf")

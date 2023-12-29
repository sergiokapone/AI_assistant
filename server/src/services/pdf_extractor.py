import tempfile
from typing import Union

import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

chroma = Chroma()
# Chunking the text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


async def pdf_extractor(
    pdf_sources: list[Union[str, bytes, tempfile.SpooledTemporaryFile]],
):
    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""
        page_number = 0

        for page in reader.pages:
            page_number += 1
            _pdf_text += page.extract_text() + "\n"

        # Разбиваем текст на части
        text_parts = text_splitter.split_text(_pdf_text)

        chroma_db = chroma.from_documents(text_parts)
        # Отправляем каждую часть в базу данных Chroma
        for i, part in enumerate(text_parts):
            chroma.store_vector(f"pdf_part_{i}", part)

        return chroma_db

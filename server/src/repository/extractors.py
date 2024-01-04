import re
import tempfile
import uuid
from typing import List, Union

import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import UploadedText, User

# read only digital PDF book which more 1000 sings


async def extract_text(path):
    ...


async def extract_text_from_pdf(
    current_user: User,
    pdf_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]],
    session: AsyncSession,
    chroma_helper,
) -> None:
    global collection_name
    cleaned_text_pdf = ""

    for pdf_source in pdf_sources:
        reader = PyPDF2.PdfReader(pdf_source)
        _pdf_text = ""

        for page in reader.pages:
            _pdf_text += page.extract_text()

        cleaned_text_pdf = re.sub(r"[\d/.]", "", _pdf_text)

    collection_name = f"collection_{current_user.id}"
    new_collection_persistent = chroma_helper.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=20
    )
    docs = text_splitter.split_text(cleaned_text_pdf)

    for doc in docs:
        uuid_name = uuid.uuid1()
        # print("document for", uuid_name)
        new_collection_persistent.add(ids=[str(uuid_name)], documents=doc)

    uploaded_text = UploadedText(
        user_id=current_user.id,
        uploaded_text=cleaned_text_pdf,
    )

    session.add(uploaded_text)
    await session.commit()


async def extract_text_from_txt():
    ...


async def extract_subtitles_from_youtube():
    ...

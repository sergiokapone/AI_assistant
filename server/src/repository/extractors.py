import re

import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import UploadedText, User

chroma = Chroma()
# Chunking the text
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


async def pdf_extractor(
        pdf_source: str,
        current_user: User,
        session: AsyncSession,
):
    reader = PyPDF2.PdfReader(pdf_source)
    _pdf_text = ""

    for page in reader.pages:
        _pdf_text += page.extract_text() + "\n"

    cleaned_text_pdf = re.sub(r'[\d/.]', '', _pdf_text)

    uploaded_text = UploadedText(
        user_id=current_user.id,
        uploaded_text=cleaned_text_pdf,
    )

    session.add(uploaded_text)
    await session.commit()

import re
import tempfile
import uuid
from typing import List, Union

import PyPDF2
from fastapi import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import UploadedText, User


# read only digital PDF book which more 1000 sings


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


async def extract_text_from_txt(
        current_user: User,
        text_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]],
        session: AsyncSession,
        chroma_helper,
) -> None:
    global collection_name
    text = ""

    for text_source in text_sources:
        loader = TextLoader(text_source)
        documents = loader.load()

        for document in documents:
            text += document.extract_text()

    collection_name = f"collection_{current_user.id}"
    new_collection_persistent = chroma_helper.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=20
    )
    docs = text_splitter.split_text(text)

    for doc in docs:
        uuid_name = uuid.uuid1()
        # print("document for", uuid_name)
        new_collection_persistent.add(ids=[str(uuid_name)], documents=doc)

    uploaded_text = UploadedText(
        user_id=current_user.id,
        uploaded_text=text,
    )

    session.add(uploaded_text)
    await session.commit()

# I can't found good liberalises (((( on youtube

# async def extract_subtitles_from_youtube(
#         current_user: User,
#         subtitles_sources: List[Union[str, bytes, tempfile.SpooledTemporaryFile]],
#         session: AsyncSession,
#         chroma_helper,
# ) -> None:
#     global collection_name
#     api_key = 'AIzaSyDYA6S69oK5MEVFUzfXC5G9BTvSFo4RTNI'  # Вставьте ваш API-ключ YouTube
#     video_id = "wvxlX3kAsoU&t"
#     videoURL = f'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}&key={api_key}'

    # response = requests.get(videoURL)
    # if response.status_code == 200:
    #     captions = response.json()
    #     if captions.get('items'):
    #         subtitle_url = captions['items'][0]['snippet']['url']
    #         subtitle_text = requests.get(subtitle_url).text
    #         return subtitle_text
    # return ""

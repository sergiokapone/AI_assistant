from chromadb import PersistentClient, Settings

chroma_client = None


def initialize_chroma_client():
    global chroma_client

    if chroma_client is None:
        chroma_client = PersistentClient(
            path="chromadb", settings=Settings(allow_reset=True)
        )

    return chroma_client


def get_chroma_client():
    return initialize_chroma_client()

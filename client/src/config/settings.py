from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str = "http://127.0.0.1:8000/api/v1/"
    sign_in_url: str = base_url + "auth/login/"
    sign_up_url: str = base_url + "auth/signup/"
    chat_url: str = base_url + "chat"
    uload_file_url: str = base_url + "upload_pdf/"
    llm_selector_url: str = base_url + "llm_selector/"


settings = Settings()

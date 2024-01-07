from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str = "http://127.0.0.1:8000/api/v1/"
    sign_up_url: str = base_url + "auth/signup/"
    sign_in_url: str = base_url + "auth/login/"
    log_out_url: str = base_url + "auth/logout/"
    chat_url: str = base_url + "chat"
    uload_file_url: str = base_url + "upload_pdf/"
    llm_selector_url: str = base_url + "llm_selector/"
    get_history_url: str = base_url + "get_history/"


settings = Settings()

from enum import Enum


class LLMNameEnum(str, Enum):
    llm_option1: str = "databricks/dolly-v2-3b"
    llm_option2: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"

from enum import Enum


class LLMNameEnum(str, Enum):
    llm_option1 = "databricks/dolly-v2-3b"
    llm_option2 = "mistralai/Mixtral-8x7B-Instruct-v0.1"

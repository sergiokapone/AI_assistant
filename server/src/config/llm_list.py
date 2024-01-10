from enum import Enum


class LLMNameEnum(str, Enum):
    llm_option1: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm_option2: str = "HuggingFaceH4/zephyr-7b-beta"

from dotenv import load_dotenv
from abc import ABC, abstractmethod
from dataclasses import dataclass
import os 
from openai import OpenAI

load_dotenv()   
@dataclass
class LLMConfig:
    """
    LLM configuration class.

    Attributes:
        model_name (str): The name of the model to use.
        base_url (str): The base URL for the API.
        api_key (str): The API key for authentication.
        temperature (float): The temperature parameter for the model.
        max_tokens (int): The maximum number of tokens to generate.
    """


    model_name: str = os.getenv("MODEL_NAME")
    base_url: str = os.getenv("BASE_URL")
    api_key: str = os.getenv("API_KEY")
    temperature: float = float(os.getenv("TEMPERATURE", "0.5"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))
    
class LLMClient(ABC):
    """
    LLM client class.

    Attributes:
        config (LLMConfig): The configuration for the LLM.
    """
    def __init__(self, config: LLMConfig):
        self.config = config
    
    def openai_client(self):
        """
        Get the OpenAI client.

        Returns:
            OpenAI: The OpenAI client.
        """
        try:
            
            model =  OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
            )
            
            return model
        except Exception as e:
            return e
            
    def client(self):
        print(self.config.api_key)
        return self.openai_client()
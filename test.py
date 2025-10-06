from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client =  OpenAI(
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL")
            )

# Gọi Chat Completions
response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),  # có thể thay bằng gpt-4.1 hoặc gpt-3.5-turbo tuỳ nhu cầu
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about the ocean."}
    ],
    temperature=0.7
)

# In ra kết quả
print(response.choices[0].message.content)


    # model_name: str = os.getenv("MODEL_NAME")
    # base_url: str = os.getenv("BASE_URL")
    # api_key: str = os.getenv("API_KEY")
from src.node.client import LLMConfig,LLMClient
from abc import ABC, abstractmethod
import json
from utils.build_prompt import build_block_prompt
import os
from openai import OpenAI

class BaseLoader:
    def __init__(self,config_path):
        self.config = self.load_json(config_path)
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.set_role()
    
    def load_json(self,path:str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config
        except Exception as e:
            return f"Error: {e}"
                
    def set_role(self):
        try:
            
            self.conversation[0]['content'] = self.config['system_role']
        except Exception as e:
            print(f"Eror:{e}")
    def run(self,conversation):

        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=conversation,
            max_tokens=self.config.max_tokens,
        )
        return response.choices[0].message.content
        
    @abstractmethod 
    def execute(self):
        pass

class NodeLoader(BaseLoader):
    def __init__(self, config_path):
        super().__init__(config_path)
    
    def execute(self,question=None,history:list=None,function=None):
        
        self.config['input']['user_question'] = question

        if history is not None:
            self.conversation = history
        else:
            prompt = build_block_prompt(self.config)
            
        print(prompt)

        self.conversation.append({"role": "user","content": prompt})

        client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=self.conversation,
            max_tokens=4096,
        )
        
        messages = response.choices[0].message.content
        
        return messages
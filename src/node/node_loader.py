from src.node.client import LLMConfig,LLMClient
from abc import ABC, abstractmethod
import json
from utils.build_json_promt import build_block_prompt

class BaseLoader:
    def __init__(self,config_path):
        self.config = LLMConfig()
        self.client = LLMClient(self.config)
        self.config = self.load_json(config_path)
        self.conversation = [{"role": "system", "content": "You are a helpful assistant."}]
        self.set_role()
    
    def load_json(self,path:str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.loads(f)
                print(config)
                return config
        except Exception as e:
            return f"Error: {e}"
                
    def set_role(self):
        print(self.config['role'])
        try:
            
            self.conversation[0]['content'] = self.config['role']
        except Exception as e:
            print(f"Eror:{e}") 
        
    @abstractmethod 
    def execute(self):
        pass

class NodeLoader(BaseLoader):
    def __init__(self, config_path):
        super().__init__(config_path)
    
    def execute(self,question,history:list=None):
        if history is not None:
            self.conversation = history
        else:
            prompt = build_block_prompt()
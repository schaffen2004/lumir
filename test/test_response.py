from src.node.node_loader import NodeLoader

node = NodeLoader("/home/schaffen/Workspace/Project/lumir/config/lumir.json")
response = node.execute("Hello")

print(response)
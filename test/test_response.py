from src.node.node_loader import NodeLoader


class NodeClient:
    def __init__(self, config_path):
        self.node_loader = NodeLoader(config_path)
        self.conversation_history = []

    def query(self, message, preserve_history=True):
        if preserve_history:
            history = self.conversation_history if self.conversation_history else None
        else:
            history = None

        response = self.node_loader.execute(message, history)

        if preserve_history:
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def clear_history(self):
        self.conversation_history = []

    def get_history(self):
        return self.conversation_history.copy()


if __name__ == "__main__":
    client = NodeClient("/home/schaffen/Workspace/Project/lumir/config/decompose.json")

    response = client.query("Lumir là gì?")
    print(response)
import os
import json

class FileManager:

    def __init__(self, path: str):
        self.path = f"./localdb/{path}.json"

        if not os.path.exists(self.path):
            with open(self.path, 'a') as f:
                f.write(json.dumps({}))

    
    def save(self, content: dict):
        with open(self.path, 'w') as f:
            f.write(json.dumps(content))

    def get(self):
        result = {}
        with open(self.path) as f:
            result = f.read()
    
        return json.loads(result)


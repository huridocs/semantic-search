import json


def loadJSON(path: str):
    with open(path, 'r') as f:
        return json.load(f)

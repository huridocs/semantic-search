from typing import List, Dict
import re


class Preprocessor:

    def __init__(self, config: Dict[str, bool]) -> None:
        for key, value in config.items():
            setattr(self, key, value)

    def rm_specialChars(self, text: str) -> str:
        return re.sub('[^a-zA-Z0-9 ]+', ' ', text)

    def rm_numbers(self, text: str) -> str:
        return re.sub(r'\d+', '', text)

    def lower(self, text: str) -> str:
        return text.lower()

    def tokenize(self, text: str) -> List[str]:
        return text.split()

    def process(self, text: str) -> str:
        if self.LOWER:
            text = self.lower(text)
        if self.RM_NUMBERS:
            text = self.rm_numbers(text)
        return text

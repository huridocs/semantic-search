from typing import List, Dict
import re
from semantic_search.TimeTracker import TimeTracker

time_tracker = TimeTracker()


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

    def replace_linebreaks(self, text: str) -> str:
        replace_double_breaks = re.sub('\n\n', 'xxxx', text)
        fixed_single_breaks = re.sub('\n', ' ', replace_double_breaks)
        fixed_double_breaks = re.sub('xxxx', '\n', fixed_single_breaks)
        return fixed_double_breaks

    def apply_functions(self, text: str, attribute: str) -> str:
        if self.__getattribute__(attribute):
            func = self.__getattribute__(attribute.lower())
            return func(text)
        return text

    @time_tracker.time_track()
    def process(self, text: str) -> str:
        attributes = self.__dict__.keys()
        for attribute in attributes:
            text = self.apply_functions(text, attribute)
        return text

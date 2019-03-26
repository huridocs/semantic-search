from typing import List
from semantic_search.osHelper import loadJSON
from semantic_search.TimeTracker import TimeTracker
import fastText
import numpy as np


time_tracker = TimeTracker()


class WordEmbedding:

    def __init__(self):
        pass

    @time_tracker.time_track()
    def load(self, model_id: str):
        config = loadJSON('models.json')
        model_path: str = config[model_id]
        self.model = fastText.load_model(model_path)

    def embed_sentence(self, sentence: str):
        tokens = sentence.split()
        vectors = [self.embed(word) for word in tokens]
        return np.average(np.array(vectors), axis=0)

    def embed(self, word: str):
        return self.model.get_word_vector(word)

    @time_tracker.time_track()
    def embed_sentences(self, sentences: List[str]):
        return [self.embed_sentence(sentence) for sentence in sentences]

    def cosine(self, vec_1: List[float], vec_2: List[float]):
        return float(np.dot(vec_1, vec_2)/(np.linalg.norm(vec_1) * np.linalg.norm(vec_2)))

    @time_tracker.time_track()
    def similarity(self, evd_emb, sentences_emb):
        return [self.cosine(evd_emb, sent_emb) for sent_emb in sentences_emb]

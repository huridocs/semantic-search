from typing import List
from semantic_search.osHelper import loadJSON
from semantic_search.TimeTracker import TimeTracker
import fasttext
import numpy as np
import math
import sys


time_tracker = TimeTracker()


class WordEmbedding:

    def __init__(self):
        pass

    @time_tracker.time_track()
    def load(self, model_id: str = 'sample', model_path: str = None):
        if model_path is None:
            config = loadJSON('models.json')
            model_path: str = config[model_id]
        self.model = fasttext.load_model(model_path)

    def embed_sentence(self, sentence: str, window: int = sys.maxsize):
        tokens = sentence.split()
        vectors = [self.embed(word) for word in tokens]

        overlap = round(window/2)
        n_windows = math.ceil(len(tokens)/overlap) - 1
        if n_windows == 0:
            n_windows = 1

        averages = []
        for i in range(n_windows):
            idx = i*overlap
            curr_vec = vectors[idx:idx+window]
            averages.append(np.average(np.array(curr_vec), axis=0))
        return averages

    def embed(self, word: str):
        return self.model.get_word_vector(word)

    @time_tracker.time_track()
    def embed_sentences(self, sentences: List[str], window: int = sys.maxsize):
        return [self.embed_sentence(sentence, window) for sentence in sentences]

    def cosine(self, vec_1: List[float], vec_2: List[float]):
        return float(np.dot(vec_1, vec_2)/(np.linalg.norm(vec_1) * np.linalg.norm(vec_2)))

    def sentence_similarity(self, evd_emb, sentence_emb):
        similarities = [self.cosine(evd_emb, window) for window in sentence_emb]
        return max(similarities)

    @time_tracker.time_track()
    def similarity(self, evd_emb, sentences_emb):
        return [self.sentence_similarity(evd_emb, sent_emb) for sent_emb in sentences_emb]

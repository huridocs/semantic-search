from semantic_search.WordEmbedding import WordEmbedding
from semantic_search.Preprocessor import Preprocessor
from semantic_search.SentenceTokenizer import SentenceTokenizer
from semantic_search.osHelper import loadJSON
import argparse
import time
from semantic_search.TimeTracker import TimeTracker


time_tracker = TimeTracker(True)


@time_tracker.time_track()
def search(search_concept, doc, embedding=None, model_id=None, config_file=None):

    if not config_file:
        config_file = 'config.json'
    config = loadJSON(config_file)

    if not model_id:
        model_id = config['DEFAULT_MODEL']

    if not embedding:
        embedding = WordEmbedding()
        embedding.load(model_id)

    preprocessor = Preprocessor(config['PREPROCESSING'])
    doc = preprocessor.process(doc)

    sentenceTokenizer = SentenceTokenizer()
    sentences = sentenceTokenizer.tokenize(doc)

    sentences_embed = embedding.embed_sentences(sentences + [search_concept])
    search_embed = sentences_embed[-1]

    similarities = embedding.similarity(search_embed, sentences_embed)

    return list(zip(sentences, similarities))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('search_concept', type=str)
    parser.add_argument('path', type=str)
    parser.add_argument('--text', action='store_true')

    arg = parser.parse_args()
    if arg.text:
        text = arg.path
    else:
        with open(arg.path, 'r') as f:
            text = f.read()

    results = search(arg.search_concept, text)
    for sentence, sim in results:
        print('{} - {}'.format(round(sim, 4), sentence))

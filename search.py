from semantic_search.WordEmbedding import WordEmbedding
from semantic_search.Preprocessor import Preprocessor
from semantic_search.SentenceTokenizer import SentenceTokenizer
from semantic_search.osHelper import loadJSON
import argparse


def search(search: str, doc: str, model_id: str = None):

    config = loadJSON('config.json')

    if not model_id:
        model_id: str = config['DEFAULT_MODEL']

    we = WordEmbedding()
    we.load(model_id)

    preprocessor = Preprocessor(config['PREPROCESSING'])
    doc = preprocessor.process(doc)
    sentenceTokenizer = SentenceTokenizer()
    sentences = sentenceTokenizer.tokenize(doc)

    search_embed = we.embed_sentence(search)
    sentences_embed = [we.embed_sentence(sentence) for sentence in sentences]
    similarities = we.similarity(search_embed, sentences_embed)

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

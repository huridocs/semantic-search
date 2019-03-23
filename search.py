from semantic_search.WordEmbedding import WordEmbedding
from semantic_search.Preprocessor import Preprocessor
from semantic_search.SentenceTokenizer import SentenceTokenizer
from semantic_search.osHelper import loadJSON
import argparse
import time


def search(search_concept, doc, embedding=None, model_id=None, config_file=None):

    t0 = time.time()
    if not config_file:
        config_file = 'config.json'
    config = loadJSON(config_file)

    if not model_id:
        model_id = config['DEFAULT_MODEL']
    print('LOAD CONFIG:     {}'.format(time.time() - t0))

    t0 = time.time()
    if not embedding:
        embedding = WordEmbedding()
        embedding.load(model_id)
    print('LOAD WORD EMBEDDINGS:    {}'.format(time.time() - t0))

    t0 = time.time()
    preprocessor = Preprocessor(config['PREPROCESSING'])
    doc = preprocessor.process(doc)
    print('PROCESS DOCS:     {}'.format(time.time() - t0))

    t0 = time.time()
    sentenceTokenizer = SentenceTokenizer()
    sentences = sentenceTokenizer.tokenize(doc)
    print('TOKENIZE IN SENTENCES:   {}'.format(time.time() - t0))

    t0 = time.time()
    search_embed = embedding.embed_sentence(search_concept)
    print('EMBED SEARCH CONCEPT:    {}'.format(time.time() - t0))

    t0 = time.time()
    sentences_embed = [embedding.embed_sentence(sentence) for sentence in sentences]
    print('EMBED SENTENCES:     {}'.format(time.time() - t0))

    t0 = time.time()
    similarities = embedding.similarity(search_embed, sentences_embed)
    print('COMPUTE SIMILARITIES:     {}'.format(time.time() - t0))

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

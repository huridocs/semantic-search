from flask import Flask, request, jsonify, make_response
from search import search
from semantic_search.WordEmbedding import WordEmbedding
from semantic_search.TimeTracker import TimeTracker
from semantic_search.osHelper import loadJSON
import json

app = Flask(__name__)

CONFIG_FILE = 'config.json'
config = loadJSON(CONFIG_FILE)

embedding = WordEmbedding()
embedding.load(model_id=config['DEFAULT_MODEL'])

time_tracker = TimeTracker()


@app.route('/semanticSearch/searchOneDoc', methods=['POST'])
@time_tracker.time_track()
def search_one_doc():
    data = json.loads(request.data)
    contents = data['contents']

    res = []
    for page in contents.keys():
        print('Page {}'.format(page))
        page_res = search(data['searchTerm'], contents[page], embedding)
        for sentence, score in page_res:
            res.append({'page': page, 'text': sentence, 'score': score})
        print('')
    return make_response(jsonify(res), 200)

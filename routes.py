from flask import Flask, request, jsonify, make_response
from search import search
import time
import json

app = Flask(__name__)


@app.route('/semanticSearch/searchOneDoc', methods=['POST'])
def search_one_doc():
    data = json.loads(request.data)
    contents = data['contents']

    t0 = time.time()
    res = []
    for page in contents.keys():
        print('NEW PAGE')
        page_res = search(data['searchTerm'], contents[page])
        for sentence, score in page_res:
            res.append({'page': int(page), 'text': sentence, 'score': score})
        print('\n')

    print('TOTAL TIME: {}'.format(time.time() - t0))
    return make_response(jsonify(res), 200)

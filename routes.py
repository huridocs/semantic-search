from flask import Flask, request, jsonify, make_response
from search import search
from systemd import journal
import time

app = Flask(__name__)

@app.route('/semanticSearch/searchOneDoc', methods=['POST'])
def search_one_doc():
    t0 = time.time()

    data = json.loads(request.data)
    search_concept = data['search_concept']
    doc = data['doc']

    sentences = search(search_concept, doc)
    journal.send('TIME: {}'.format(time-time() - t0))

    return make_response(jsonify(sentences)), 500



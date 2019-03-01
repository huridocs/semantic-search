from routes import app
import unittest
import json


first_page = "First sentence of the first page. Second sentence of the first page."
second_page = "Second page with content. Multiple sentences about migrant rights. Rights of minorities are also included."
NR_SENTENCE_LENGTH = 5
target_keys = ['text', 'score', 'page']

request = {"searchTerm": "migrant rights",
           "contents": {"1": first_page, "2": second_page}}


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_search_one_doc(self):
        resp = self.client.post('/semanticSearch/searchOneDoc', json=request)
        self.assertEqual(resp.status, '200 OK')

        data = json.loads(resp.data)
        self.assertEqual(len(data), NR_SENTENCE_LENGTH)
        self.assertEqual(set(data[0].keys()), set(target_keys))

        texts = ' '.join(list(map(lambda x: x['text'], data)))
        pages = list(map(lambda x: x['page'], data))
        self.assertEqual(pages, [1, 1, 2, 2, 2])
        self.assertEqual(texts, ' '.join([first_page, second_page]))


if __name__ == '__main__':
    unittest.main()



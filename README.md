## semantic-search

Use word embeddings to search for related concepts in a document.

### Installation

This code requires Python 3.6 and the fastText Python wrapper. Pip is the easiest way to install fastText*:

```
$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ pip install .
```

For using setuptools to install fastText follow the installing instructions [here](https://github.com/facebookresearch/fastText/tree/master/python).

Install the other dependencies with:

```
pip install -r requirements.txt
```



### Setup

This package comes without a pretrained fastText model. However you can download models of different languages [here](https://fasttext.cc/docs/en/crawl-vectors.html) or use your own model.
Make sure to create a *models/* directory in the main folder and store its .bin file there

```
 $ mkdir models
```

In the *config.json* file change the name of the DEFAULT_MODEL and your processing parameters:

```
   1 {
   2         "DEFAULT_MODEL": "hr",
   3 
   4         "PREPROCESSING": {
   5             "RM_NUMBERS": false,
   6             "LOWER": false
   7         },
   8 
   9         "SIMILARITY": {
  10             "WEIGHTED_AVG": false
  11         }
  12 }
```



### Get started

After setting everything up you can search for a concept in a selected text file with:

```
$ python search.py [search-concept] [path-to-file]
```

For example, the command for searching for *rights of minorities* in the provided sample is as follows:

```
$ python search.py 'human rights of minorities' 'tests/HRC.txt'
```

If you want to directly pass a text instead of a file add the `--text` flag:

```
$ python search.py 'human rights of minorities' 'full text' --text
```

The algorithm return for each sentence a value that indicates its similar with the search concept. The higher the value the more similar they are.

For example:

```
0.7596 - Forum on Minority Issues the Human Rights Council, ...
0.6511 - Economic and Social Council resolution 1995/31 of 25 July 1995 and ....
0.5502 - Decides to review the work of the Forum after four years.
0.4284 - [Adopted without a vote] 21st meeting 28 September 2007
```



### Testing

```
$ nose tests/
```




## semantic-search

Use word embeddings to search for related concepts in a document.



### Get started

After installing the module you can search for a concept in a selected text file with:

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



### Prerequisites

This code requires Python 3.6 and the Fastext Python wrapper. Follow the installing instructions [here](https://github.com/facebookresearch/fastText/tree/master/python).

Install other dependencies with:

```
pip install -r requirements.txt
```


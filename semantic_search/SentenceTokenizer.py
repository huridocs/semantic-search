import nltk
import numpy as np

import numpy.core.numeric as _nx
from nltk.tokenize import word_tokenize
from semantic_search.TimeTracker import TimeTracker
import re
import pdb

LEGAL_ABBREVATIONS = ['chap', 'distr', 'paras', 'cf', 'cfr', 'para', 'no', 'al', 'br', 'dr', 'hon', 'app', 'cr', 'crim', 'l.r', 'cri', 'cap', 'e.g', 'vol', 'd', 'a', 'ph', 'inc.v', 'prof', 'mrs', 'mrt', 'msn', 'mrj', 'msi', 'mrg', 'mra', 'mst', 'mrd', 'pp', 'seq', 'art', 'p', 'nos', 'op', 'i.e', 'tel']

time_tracker = TimeTracker(True)


class SentenceTokenizer:

    def __init__(self, MAX_SENTENCE_LENGTH=40, MIN_SENTENCE_LENGTH=4):
        self.MAX_SENTENCE_LENGTH = MAX_SENTENCE_LENGTH
        self.MIN_SENTENCE_LENGTH = MIN_SENTENCE_LENGTH
        self.setupTokenizer()

    def setupTokenizer(self):
        self.loadTokenizer()
        self.addAbbrevations(LEGAL_ABBREVATIONS)

    def loadTokenizer(self, language='english'):
        self.tokenizer = nltk.data.load('nltk:tokenizers/punkt/{}.pickle'.format(language))

    def addAbbrevations(self, abbrevations=[]):
        self.tokenizer._params.abbrev_types.update(abbrevations)

    def detokenize(self, wordList):
        text = ' '.join(wordList)
        text = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", text)
        text = re.sub(r' ([.,:;?!%]+)$', r"\1", text)
        text = text.replace('[ ', '[').replace(' ]', ']')
        text = text.replace('( ', '(').replace(' )', ')')
        text = text.replace('" ', '"').replace(" '", "'")
        return text.strip()

    def splitListAtPunctuationWithVarianz(self, wordList, sections, wordRange=5):
        import pdb
        #pdb.set_trace()
        wordsPerSection, extras = divmod(len(wordList), round(sections))
        sectionSizes = ([0] + extras * [wordsPerSection+1] + (wordsPerSection-extras) * [wordsPerSection])
        divInd = _nx.array(sectionSizes).cumsum()
        divInd = [ind for ind in divInd if ind <= len(wordList)]
        for indPos, pos in enumerate(divInd[1:len(divInd)-1]):
            wordListPart = wordList[pos-wordRange:pos+wordRange]
            indices = range(pos-wordRange, pos+wordRange+1)
            for wordPos, word in enumerate(wordListPart):
                if word == ',' or word == ')' or word == ']':
                    divInd[indPos+1] = indices[wordPos+1]
        splittedList = np.array_split(wordList, divInd)
        return splittedList

    def insertSpaceAfterPunctuation(self, text):
        text = re.sub(r'\.(?=[A-Z0-9])', '. ', text)
        text = re.sub(r'\)(?=[A-Z0-9])', ') ', text)
        text = re.sub(r'(?<=[a-zA-Z0-9])\(', ' (', text)
        text = re.sub(r'\](?=[A-Z0-9])', '] ', text)
        return re.sub(r',(?=[a-zA-Z0-9])', ', ', text)

    def insertNewlineAfterSpeech(self, text):
        #text = re.sub(ur'\.\u2019', ur'.\u2019\n', text)
        #text = re.sub(ur'\.\u201d', ur'.\u201d\n', text)
        return text

    def insertNewLine(self, text, indicator, minimumSentenceLength):
        previousPos = 0
        shift = 0
        for match in re.finditer(indicator, text):
            pos = match.end(0)
            if len(text[previousPos:pos].split()) >= minimumSentenceLength:
                text = text[:pos + shift] + ' \n ' + text[pos + shift:]
                previousPos = pos
                shift += 3
        return text

    def splitAtNewline(self, sentences):
        sentences = [sentence.split('\n') for sentence in sentences]
        return sum(sentences, [])

    def splitInChunks(self, sentence, MAX_SENTENCE_LENGTH):
        listOfWords = word_tokenize(sentence)
        numberOfSplits = len(listOfWords)/MAX_SENTENCE_LENGTH + 1

        splittedSentences = self.splitListAtPunctuationWithVarianz(listOfWords, numberOfSplits)
        return [self.detokenize(sentence.tolist()) for sentence in splittedSentences]

    def flattenList(self, listOfElems):
        flatList = []
        for elem in listOfElems:
            if isinstance(elem, (list,)):
                for item in elem:
                    flatList.append(item)
            else:
                flatList.append(elem)
        return flatList

    def splitTooLongSentencesAtCharacter(self, sentences, character):
        for ind, sentence in enumerate(sentences):
            if len(word_tokenize(sentence)) > self.MAX_SENTENCE_LENGTH:
                semicolonSplit = self.insertNewLine(sentence, character, self.MIN_SENTENCE_LENGTH)
                if len(semicolonSplit.split('\n')) > 1:
                    sentences[ind] = semicolonSplit.split('\n')
        return self.flattenList(sentences)

    def splitTooLongSentencesInChunks(self, sentences):
        for ind, sentence in enumerate(sentences):
            if len(word_tokenize(sentence)) > self.MAX_SENTENCE_LENGTH:
                sentences[ind] = self.splitInChunks(sentence, self.MAX_SENTENCE_LENGTH)
        return self.flattenList(sentences)

    def filterForLength(self, sentences):
        return [sentence for sentence in sentences if len(sentence.split()) >= self.MIN_SENTENCE_LENGTH]

    @time_tracker.time_track()
    def tokenize(self, text, maxSentenceLength=50, minSentenceLength=5):
        text = self.insertSpaceAfterPunctuation(text)
        text = self.insertNewlineAfterSpeech(text)
        sentences = self.tokenizer.tokenize(text)
        sentences = self.splitAtNewline(sentences)

        sentences = self.splitTooLongSentencesAtCharacter(sentences, ':')
        #sentences = splitTooLongSentencesAtCharacter(sentences, ';', minSentenceLength)

        sentences = self.splitTooLongSentencesInChunks(sentences)

        sentences = self.filterForLength(sentences)

        return sentences

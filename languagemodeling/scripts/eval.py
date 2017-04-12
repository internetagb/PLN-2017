"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""

import pickle
from docopt import docopt
from nltk.data import load
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import PlaintextCorpusReader as PCR

if __name__ == '__main__':
    # read options
    opts = docopt(__doc__)
    path = str(opts['-i'])
    # open model file
    file = open(path, 'rb')
    # load model file
    model = pickle.load(file)

    # set pattern for tokenize
    pattern = r'''(?ix)    # set flag to allow verbose regexps
        (?:Inc\.|sra\.|sr\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''

    # tokenize test corpus
    sent_tokenizer = load('tokenizers/punkt/spanish.pickle')
    tokenizer = RegexpTokenizer(pattern)
    path = '/home/alangb/Escritorio/'
    corpus = PCR(path, 'corpus_test.txt', word_tokenizer=tokenizer,
                 sent_tokenizer=sent_tokenizer)
    sents = corpus.sents()

    # calculate (and print) perplexity
    perplexity = model.perplexity(sents)
    print("Perplexity: " + str(perplexity))

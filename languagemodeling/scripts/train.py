"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
# from docopt import docopt
# import pickle

# from nltk.corpus import gutenberg

# from languagemodeling.ngram import NGram

import nltk
from nltk.corpus import PlaintextCorpusReader as PCR
from nltk.tokenize import RegexpTokenizer

if __name__ == '__main__':
    # opts = docopt(__doc__)

    pattern = r'''(?ix)    # set flag to allow verbose regexps
        (?:Inc\.|sra\.|sr\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''

    sent_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

    tokenizer = RegexpTokenizer(pattern)

    path = '/home/alangb/Escritorio/'

    corpus = PCR(path, 'corpus.txt', word_tokenizer=tokenizer,
                 sent_tokenizer=sent_tokenizer)

    for i in range(5):
        print("\n")
        print(corpus.sents()[i])

    # # load the data
    # sents = gutenberg.sents('austen-emma.txt')

    # # train the model
    # n = int(opts['-n'])
    # model = NGram(n, sents)

    #   # save it
    # filename = opts['-o']
    # f = open(filename, 'wb')
    # pickle.dump(model, f)
    # f.close()

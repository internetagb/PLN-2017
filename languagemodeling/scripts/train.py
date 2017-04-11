"""
Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""

import pickle
from docopt import docopt
from nltk.data import load
from languagemodeling.ngram import NGram
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import PlaintextCorpusReader as PCR

if __name__ == '__main__':
    opts = docopt(__doc__)

    pattern = r'''(?ix)    # set flag to allow verbose regexps
        (?:Inc\.|sra\.|sr\.)
        | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*        # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''

    # load the data
    sent_tokenizer = load('tokenizers/punkt/spanish.pickle')

    tokenizer = RegexpTokenizer(pattern)

    path = '/home/alangb/Escritorio/'

    corpus = PCR(path, 'corpus.txt', word_tokenizer=tokenizer,
                 sent_tokenizer=sent_tokenizer)

    sents = corpus.sents()

    # train the model
    n = int(opts['-n'])
    model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()

"""
Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""

import pickle
from docopt import docopt
from languagemodeling.ngram import NGram, NGramGenerator
# from nltk.corpus import PlaintextCorpusReader as PCR
# from nltk.tokenize import RegexpTokenizer

if __name__ == '__main__':
    opts = docopt(__doc__)

    path = str(opts['-i'])
    n = int(opts['-n'])

    file = open(path, 'rb')

    model = pickle.load(file)

    generator = NGramGenerator(model)

    for _ in range(n):
        print("\n")
        print(' '.join(generator.generate_sent()))

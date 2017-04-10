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

    path2 = "/home/alangb/Escritorio/out.txt"
    output = open(path2, 'w')
    for _ in range(n):
        output.write(' '.join(generator.generate_sent())+"\n")
    output.close()
    file.close()

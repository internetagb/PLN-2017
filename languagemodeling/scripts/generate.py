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
from languagemodeling.ngram import NGramGenerator

if __name__ == '__main__':
    opts = docopt(__doc__)
    # read options
    path = str(opts['-i'])
    n = int(opts['-n'])
    # open model file
    file = open(path, 'rb')
    # load model file
    model = pickle.load(file)
    # create generator
    generator = NGramGenerator(model)
    # print sentences while generate them.
    for _ in range(n):
        print(' '.join(generator.generate_sent())+"\n")

"""Train a parser.

Usage:
  train.py [-m <model>] [-n <order>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: flat]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
  -n <order>    Horizontal Markovization order [default: None]
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from corpus.ancora import SimpleAncoraCorpusReader
from parsing.upcfg import UPCFG
from parsing.baselines import Flat, RBranch, LBranch


models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
    'upcfg': UPCFG,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    path = '/home/alangb/Escritorio/ancora-3.0.1es/'
    corpus = SimpleAncoraCorpusReader(path, files)

    print('Training model...')
    n = opts['-n']
    m = opts['-m']
    if n == 'None':
        model = models[m](corpus.parsed_sents())
    else:
        model = models[m](corpus.parsed_sents(), horzMarkov=int(n))

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()

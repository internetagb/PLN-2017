"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] -c clf -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  mlhmm: Maximum Likelihood Hidden Markov Model
  -n <n>        Order of the model
  -c clf        Max. Entropy Classsifier:
                  lr: Logistic Regression
                  mnb: Multinomial NB
                  svc: Linear SVC
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM


models = {
    'base': BaselineTagger,
    'mlhmm': MLHMM,
    'memm': MEMM,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    path = '/home/alangb/Escritorio/ancora-3.0.1es/'
    corpus = SimpleAncoraCorpusReader(path, files)
    sents = list(corpus.tagged_sents())

    # train the model
    chosen_model = models[opts['-m']]
    n = opts['-n']
    if n is None:
        assert chosen_model == 'base'
        model = chosen_model(sents)
    else:
        classifier = opts['-c']
        if classifier is None:
            model = chosen_model(int(n), sents)
        else:
            model = chosen_model(int(n), sents, classifier)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()

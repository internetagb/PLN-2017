"""Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    path = '/home/alangb/Escritorio/ancora-3.0.1es/'
    corpus = SimpleAncoraCorpusReader(path, files)
    parsed_sents = list(corpus.parsed_sents())

    print('Parsing...')
    hits, total_gold, total_model = 0, 0, 0
    hitsu, total_goldu, total_modelu = 0, 0, 0
    n = opts['-n']
    m = opts['-m']
    if n is not None:
        parsed_sent = list(parsed_sents)
        parsed_sents = parsed_sents[:int(n)]
    if m is not None:
        parsed_sents = [t for t in parsed_sents if len(t.leaves()) <= int(m)]
    n = len(parsed_sents)
    format_str = '{:3.1f}% ({}/{}) | Labeled: (P={:2.2f}%, R={:2.2f}%,'
    format_str += ' F1={:2.2f}%) | Unlabeled: (P={:2.2f}%, R={:2.2f}%,'
    format_str += ' F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        gold_spans = spans(gold_parsed_sent, unary=False)
        model_spans = spans(model_parsed_sent, unary=False)
        hits += len(gold_spans & model_spans)
        total_gold += len(gold_spans)
        total_model += len(model_spans)

        # compute unlabeled scores
        unlabeled_gold = set()
        for span in gold_spans:
            unlabeled_gold.add(span[1:])

        unlabeled_model = set()
        for span in model_spans:
            unlabeled_model.add(span[1:])

        hitsu += len(unlabeled_gold & unlabeled_model)
        total_goldu += len(unlabeled_gold)
        total_modelu += len(unlabeled_model)

        # compute labeled partial results
        precl = float(hits) / total_model * 100
        recl = float(hits) / total_gold * 100
        f1l = 2 * precl * recl / (precl + recl)

        # compute unlabeled partial results
        precu = float(hitsu) / total_modelu * 100
        recu = float(hitsu) / total_goldu * 100
        f1u = 2 * precu * recu / (precu + recu)

        progress(format_str.format(float(i+1) * 100 / n,
                                   i+1, n, precl, recl, f1l, precu, recu, f1u))

    if n > 0:
        print('')
        print('Parsed {} sentences'.format(n))
        print('\nLabeled')
        print('  Precision: {:2.2f}% '.format(precl))
        print('  Recall: {:2.2f}% '.format(recl))
        print('  F1: {:2.2f}% '.format(f1l))
        print('\nUnlabeled')
        print('  Precision: {:2.2f}% '.format(precu))
        print('  Recall: {:2.2f}% '.format(recu))
        print('  F1: {:2.2f}% '.format(f1u))

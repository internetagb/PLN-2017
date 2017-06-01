"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
from collections import Counter
from corpus.ancora import SimpleAncoraCorpusReader
from sklearn.metrics import confusion_matrix


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    path = '/home/alangb/Escritorio/ancora-3.0.1es/'
    corpus = SimpleAncoraCorpusReader(path, files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total = 0, 0
    hits_u, hits_k = 0, 0
    total_u, total_k = 0, 0
    n = len(sents)
    gold_tags, model_tags = [], []  # for confusion matrix

    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        gold_tags += gold_tag_sent
        model_tags += model_tag_sent

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        # known and unknown scores
        for j in range(len(model_tag_sent)):
            if model.unknown(word_sent[j]):
                total_u += 1
            else:
                total_k += 1
            if gold_tag_sent[j] == model_tag_sent[j]:
                if model.unknown(word_sent[j]):
                    hits_u += 1
                else:
                    hits_k += 1
        acc_u = float(hits_u)/total_u
        acc_k = float(hits_k)/total_k
        progress('Completado un {:3.1f}%, Global: {:2.2f}%, Known: {:2.2f}%, '
                 'Unknown: {:2.2f}%'.format(float(i)*100 / n,
                                            acc*100, acc_k*100, acc_u*100))
    acc = float(hits) / total
    acc_u = float(hits_u)/total_u
    acc_k = float(hits_k)/total_k

    # print results
    print('\x1b[6;30;42m' + '\n\nResultados finales' + '\x1b[0m')
    print('Global accuracy: {:2.2f}%'.format(acc * 100))
    print('Known words accuracy: {:2.2f}%'.format(acc_k * 100))
    print('Unknown words accuracy: {:2.2f}%'.format(acc_u * 100))

    common_tags = [tag for tag, _ in Counter(gold_tags).most_common(10)]
    conf_matrix = confusion_matrix(gold_tags, model_tags, common_tags)
    conf_matrix = (conf_matrix/total) * 100

    # print confusion matrix
    print('\x1b[6;30;42m' + '\nMatriz de confusión\n' + '\x1b[0m')
    print(' '*10 + '|', end='')
    for i in range(len(common_tags)):
        print('{:^10}'.format(common_tags[i]), end=' |')
    print('')
    print('-'*131)
    i = 0
    values = ([round(v, 3) for v in row] for row in conf_matrix)
    for row in values:
        print('{:^10}'.format(common_tags[i]), end='|')
        print(''.join(['|'.join(['{:^11}'.format(item) for item in row])]))
        i += 1

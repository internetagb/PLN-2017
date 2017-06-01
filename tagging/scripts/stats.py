"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""

from operator import itemgetter as elem
from docopt import docopt
from collections import Counter, defaultdict
from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    path = '/home/alangb/Escritorio/ancora-3.0.1es/'
    corpus = SimpleAncoraCorpusReader(path)
    sents = list(corpus.tagged_sents())

    # compute the statistics

    # get words and tags
    words_tags = [word_tag for sent in sents for word_tag in sent]
    words, tags = zip(*words_tags)
    word_types = set(words)
    tag_types = set(tags)

    # calculate 10 most common tags
    common_tags = Counter(tags).most_common(10)

    # calculate 5 most common words
    # for each one of the most common tags
    comm_word_tag = {}
    for tag, _ in common_tags:
        words_with_tag = list(word for word, tag2 in words_tags if tag == tag2)
        comm_word_tag[tag] = Counter(words_with_tag).most_common(5)

    # calculate ambiguity levels
    amb_levels = defaultdict(list)
    word_amb = Counter([word for word, _ in set(words_tags)])
    for key, value in word_amb.items():
        amb_levels[value].append(key)

    # calculate most common words (for each ambiguity level)
    comm_w_amb = defaultdict(list)
    for word, _ in sorted(Counter(words).items(), key=elem(1), reverse=True):
        amb_lev = word_amb[word]
        if len(comm_w_amb[amb_lev]) < 5:
            comm_w_amb[amb_lev].append(word)

    # print basic stats
    print('\x1b[6;30;42m' + '\nEstadísticas básicas' + '\x1b[0m')
    print('Cantidad de oraciones: {}'.format(len(sents)))
    print('Cantidad de ocurrencias de palabras: {}'.format(len(words)))
    print('Cantidad de tipos de palabras: {}'.format(len(word_types)))
    print('Cantidad de etiquetas: {}'.format(len(tag_types)))

    # print tag stats
    print('\x1b[6;30;42m' + '\n\nEtiquetas mas frecuentes' + '\x1b[0m')
    print('-'*78)
    s = "   Tag   |  Frecuencia  | Porcentaje |  5 palabras mas frecuentes  "
    print(s)
    print('-'*78)
    for tag, count in common_tags:
        percen = str(round(float(count*100)/len(tags), 3)) + ' %'
        comm_words_tmp = [word for word, _ in comm_word_tag[tag]]
        comm_words_tmp = ', '.join([word for word in comm_words_tmp])
        print("{:^8} | {:^12} | {:^10} | {}".format(tag, count, percen,
                                                    comm_words_tmp))
    print('-'*78)

    # print ambiguity stats
    print('\x1b[6;30;42m' + '\n\nNiveles de ambigüedad' + '\x1b[0m')
    print('-'*85)
    s = " Nivel de ambigüedad |  Cantidad  | "
    s += "Porcentaje |  5 palabras mas frecuentes  "
    print(s)
    print('-'*85)
    for i in range(1, 10):
        if i in amb_levels:
            count = len(amb_levels[i])
            comm_words_tmp = ' - '.join(comm_w_amb[i])
        else:
            count = 0
            comm_words_tmp = ''
        percen = str(round(float(count*100)/len(word_types), 3)) + ' %'
        print("{:^20} | {:^10} | {:^10} | {}".format(i, count, percen,
                                                     comm_words_tmp))
    print('-'*85 + '\n')

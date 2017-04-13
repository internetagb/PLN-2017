# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from languagemodeling.ngram import NGram, NGramGenerator, AddOneNGram
from math import log

class TestExtras(TestCase):

    def setUp(self):
        self.sents = [
            'el gato come pescado .'.split(),
            'la gata come salmón .'.split(),
        ]

        self.sents2 = [
            'el gato come pescado fresco .'.split(),
            'el gato come pescado viejo .'.split(),
        ]

        self.sents3 = [
            'el gato come pescado y duerme .'.split(),
            'la gata come pescado y duerme .'.split(),
        ]

        self.sents4 = [
            'la casa se construye y el corre'.split(),
            'la gata come pescado y duerme'.split(),
            'el corre y la gata come ensalada'.split(),
        ]

    def test_count_3gram(self):
        ngram = NGram(3, self.sents)
        counts = {
            ('<s>', 'el'): 1,
            ('el', 'gato'): 1,
            ('gato', 'come'): 1,
            ('come', 'pescado'): 1,
            ('pescado', '.'): 1,
            ('<s>', '<s>'): 2,
            ('<s>', 'la'): 1,
            ('la', 'gata'): 1,
            ('gata', 'come'): 1,
            ('come', 'salmón'): 1,
            ('salmón', '.'): 1,
            ('<s>', '<s>', 'el') : 1,
            ('<s>', 'el', 'gato') : 1,
            ('el', 'gato', 'come') : 1,
            ('gato', 'come', 'pescado') : 1,
            ('come', 'pescado', '.') : 1,
            ('pescado', '.', '</s>') : 1,
            ('<s>', '<s>', 'la') : 1,
            ('<s>', 'la', 'gata') : 1,
            ('la', 'gata', 'come') : 1,
            ('gata', 'come', 'salmón') : 1,
            ('come', 'salmón', '.') : 1,
            ('salmón', '.', '</s>') : 1,
        }

        for gram, c in counts.items():
            self.assertEqual(ngram.count(gram), c)

    def test_cond_prob_3gram(self):
        ngram = NGram(3, self.sents)

        probs = {
            ('pescado', ('gato', 'come')): 1,
            ('salmón', ('gata', 'come')): 1,
            ('salame', ('gato', 'come')): 0.0,
            ('gato', ('<s>', 'el')) : 1,
            ('gata', ('<s>', 'el')) : 0.0,
        }

        for (token, prev), p in probs.items():
            self.assertEqual(ngram.cond_prob(token, list(prev)), p)


    def test_cond_prob_4gram(self):
        ngram = NGram(4, self.sents2)

        probs = {
            ('pescado', ('el','gato', 'come')): 1,
            ('salmón', ('la', 'gata', 'come')): 0.0,
            ('salame', ('el', 'gato', 'come')): 0.0,
            ('gato', ('<s>', '<s>', 'el')) : 1,
            ('viejo', ('gato','come', 'pescado')) : 0.5,
            ('fresco', ('gato','come', 'pescado')) : 0.5,
        }

        for (token, prev), p in probs.items():
            self.assertEqual(ngram.cond_prob(token, list(prev)), p)


    def test_sent_prob_3and4gram(self):
        ngram = NGram(3, self.sents3)
        ngram2 = NGram(4, self.sents3)

        sents = {
            'el gato come pescado y ronca .': 0.0, # 'ronca' unseen
            'la la la': 0.0,  # 'la' after 'la' unseen
            # la probabilidad se da por el principio,
            # si empieza con 'la' o 'el'
            'el gato come pescado y duerme . ': 0.5,
            'la gata come pescado y duerme . ': 0.5
        }

        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_prob(sent.split()), prob, msg=sent)
            self.assertAlmostEqual(ngram2.sent_prob(sent.split()), prob, msg=sent)

    def test_sent_log_prob_3and4gram(self):
        ngram = NGram(3, self.sents2)
        ngram2 = NGram(4, self.sents2)

        log2 = lambda x: log(x, 2)
        sents = {
            'el gato come pescado nuevo .': float('-inf'),  # 'nuevo' unseen
            'la la la': float('-inf'),  # 'la' after 'la' unseen
            # after 'pescado': 'viejo' and 'fresco' have prob 0.5.
            'el gato come pescado fresco . ': log2(0.5),
            'el gato come pescado viejo . ': log2(0.5)
        }
        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_log_prob(sent.split()), prob, msg=sent)
            self.assertAlmostEqual(ngram2.sent_log_prob(sent.split()), prob, msg=sent)


    def test_init_3gram(self):
        ngram = NGram(3, self.sents)
        generator = NGramGenerator(ngram)

        probs = {
            ('<s>', '<s>'): {'el': 0.5, 'la': 0.5},
            ('<s>', 'el',): {'gato': 1.0},
            ('el', 'gato'): {'come': 1.0},
            ('gato', 'come'): {'pescado': 1.0},
            ('come', 'pescado'): {'.': 1.0},
            ('pescado', '.'): {'</s>': 1.0},
            ('<s>', 'la'): {'gata': 1.0},
            ('la', 'gata'): {'come': 1.0},
            ('gata', 'come'): {'salmón': 1.0},
            ('come', 'salmón'): {'.': 1.0},
            ('salmón', '.'): {'</s>': 1.0},

        }
        sorted_probs = {
            ('<s>', '<s>'): [('el', 0.5), ('la', 0.5)],
            ('<s>', 'el',): [('gato', 1.0)],
            ('el', 'gato'): [('come', 1.0)],
            ('gato', 'come'): [('pescado', 1.0)],
            ('come', 'pescado'): [('.', 1.0)],
            ('pescado', '.'): [('</s>', 1.0)],
            ('<s>', 'la'): [('gata', 1.0)],
            ('la', 'gata'): [('come', 1.0)],
            ('gata', 'come'): [('salmón', 1.0)],
            ('come', 'salmón'): [('.', 1.0)],
            ('salmón', '.'): [('</s>', 1.0)],
        }

        self.assertEqual(dict(generator.probs), probs)
        self.assertEqual(generator.sorted_probs, sorted_probs)


    def test_generate_token_3and4gram(self):
        ngram = NGram(3, self.sents3)
        ngram2 = NGram(4, self.sents3)
        generator = NGramGenerator(ngram)
        generator2 = NGramGenerator(ngram2)

        for i in range(100):
            # after 'come pescado' always comes 'y'
            token = generator.generate_token(('come','pescado'))
            self.assertEqual(token, 'y')
            # after 'come pescado y' always comes 'duerme'
            token = generator2.generate_token(('come','pescado', 'y'))
            self.assertEqual(token, 'duerme')
            # sentence may come start with 'el' or 'la'
            token = generator.generate_token(('<s>', '<s>'))
            self.assertTrue(token in ['el', 'la'])
            token = generator2.generate_token(('<s>', '<s>', '<s>'))
            self.assertTrue(token in ['el', 'la'])

    def test_generate_sent_3and4gram(self):
        ngram = NGram(3, self.sents4)
        ngram2 = NGram(4, self.sents4)
        generator = NGramGenerator(ngram)
        generator2 = NGramGenerator(ngram2)

        # all the possible generated sentences for 3 or 4-grams:
        sents = [
            'la casa se construye y el corre y la gata come ensalada',
            'el corre y la gata come pescado y duerme',
            'la casa se construye y el corre y la gata come ensalada',
            'la casa se construye y el corre y la gata come pescado y duerme',
            'la casa se construye y el corre',
            'la gata come pescado y duerme',
            'el corre y la gata come ensalada',
            'el corre',
            'la gata come ensalada',
            'la casa se construye y el corre',
            'la gata come pescado y duerme',
        ]

        for i in range(1000):
            sent = generator.generate_sent()
            sent2 = generator2.generate_sent()
            self.assertTrue(' '.join(sent) in sents)
            self.assertTrue(' '.join(sent2) in sents)

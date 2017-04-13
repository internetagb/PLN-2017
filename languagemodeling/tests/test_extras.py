# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from languagemodeling.ngram import NGram, NGramGenerator, AddOneNGram

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


    def test_sent_prob_3gram(self):
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

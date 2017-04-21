# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from languagemodeling.ngram import NGram, InterpolatedNGram
from math import log


class TestExtras2(TestCase):

    def setUp(self):
        self.sents = [
            'el gato come pescado .'.split(),
            'la gata come salmón .'.split(),
        ]

    def test_count_3gram(self):
        ngram = InterpolatedNGram(3, self.sents, gamma=1.0)

        counts = {
            (): 12,
            ('el',): 1,
            ('gato',): 1,
            ('come',): 2,
            ('pescado',): 1,
            ('.',): 2,
            ('</s>',): 2,
            ('la',): 1,
            ('gata',): 1,
            ('salmón',): 1,
            ('<s>', 'el'): 1,
            ('el', 'gato'): 1,
            ('gato', 'come'): 1,
            ('come', 'pescado'): 1,
            ('pescado', '.'): 1,
            ('.', '</s>'): 2,
            ('<s>', 'la'): 1,
            ('la', 'gata'): 1,
            ('gata', 'come'): 1,
            ('come', 'salmón'): 1,
            ('salmón', '.'): 1,
            ('<s>', '<s>', 'el'): 1,
            ('<s>', 'el', 'gato'): 1,
            ('el', 'gato', 'come'): 1,
            ('gato', 'come', 'pescado'): 1,
            ('come', 'pescado', '.'): 1,
            ('pescado', '.', '</s>'): 1,
            ('<s>', '<s>', 'la'): 1,
            ('<s>', 'la', 'gata'): 1,
            ('la', 'gata', 'come'): 1,
            ('gata', 'come', 'salmón'): 1,
            ('come', 'salmón', '.'): 1,
            ('salmón', '.', '</s>'): 1,
        }
        for gram, c in counts.items():
            self.assertEqual(ngram.count(gram), c, gram)


    def test_held_out_2gram(self):
        model = InterpolatedNGram(2, self.sents)

        # only first sentence (second sentence is held-out data)
        counts = {
            (): 6,
            ('el',): 1,
            ('gato',): 1,
            ('come',): 1,
            ('pescado',): 1,
            ('.',): 1,
            ('</s>',): 1,
            ('<s>', 'el'): 1,
            ('el', 'gato'): 1,
            ('gato', 'come'): 1,
            ('come', 'pescado'): 1,
            ('pescado', '.'): 1,
            ('.', '</s>'): 1,
        }
        for gram, c in counts.items():
            self.assertEqual(model.count(gram), c, gram)

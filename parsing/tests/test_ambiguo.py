# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log2
from nltk.tree import Tree
from nltk.grammar import PCFG

from parsing.cky_parser import CKYParser


class TestCKYParser(TestCase):

    def test_parse(self):
        grammar = PCFG.fromstring(
            """
                S -> Noun VP            [1.0]
                VP -> VP Vbg            [0.7]
                VP -> Verb PP           [0.3]
                PP -> Prep Noun         [0.8]
                PP -> Prep NP           [0.2]
                NP -> Noun Vgb          [1.0]
                Noun -> 'Mario'         [0.6]
                Noun -> 'Jonathan'      [0.4]
                Verb -> 'espía'         [1.0]
                Vbg -> 'corriendo'      [1.0]
                Prep -> 'a'             [1.0]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('Mario espía a Jonathan corriendo'.split())

        # check tree
        t2 = Tree.fromstring(
            """
                (S
                    (Noun Mario)
                    (VP (VP (Verb espía)
                            (PP (Prep a)
                                (Noun Jonathan)))
                        (Vbg corriendo))
                )
            """)
        self.assertEqual(t, t2)

        # El otro arbol posible sería:
        # t3 = Tree.fromstring(
        #     """
        #         (S
        #             (Noun Mario)
        #             (VP (Verb espía)
        #                 (PP (Prep a)
        #                     (NP (Noun Jonathan)
        #                         (Vbg corriendo))))
        #         )
        #     """)

        # check log probability
        lp2 = log2(1.0 * 0.7 * 0.3 * 0.8 * 0.6 * 1.0 * 1.0 * 0.4 * 1.0)
        self.assertAlmostEqual(lp, lp2)

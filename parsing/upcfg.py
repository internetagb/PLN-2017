from parsing.util import unlexicalize, lexicalize
from collections import defaultdict
from nltk.grammar import ProbabilisticProduction as PP, PCFG, Nonterminal as N
from parsing.cky_parser import CKYParser
from parsing.baselines import Flat


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence', horzMarkov=None):
        """
        parsed_sents -- list of training trees.
        """
        countsX = defaultdict(int)
        countsYZ = defaultdict(lambda: defaultdict(int))
        ut = [unlexicalize(t.copy(deep=True)) for t in parsed_sents]
        self.prods = prods = []
        self.start = start

        # initialize list of productions
        for t in ut:
            t.chomsky_normal_form(horzMarkov=horzMarkov)
            t.collapse_unary(collapsePOS=True)
            for p in t.productions():
                X = p.lhs()
                YZ = p.rhs()
                countsX[X] += 1
                countsYZ[X][YZ] += 1
        for (x, v) in countsX.items():
            for key in countsYZ[x].keys():
                prods.append(PP(x, key, prob=countsYZ[x][key] / v))

        self.parser = CKYParser(PCFG(N(start), prods))

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        sent, tags = zip(*tagged_sent)
        prob, tree = self.parser.parse(tags)
        if prob == float('-inf'):
            tree = Flat([], self.start).parse(tagged_sent)
        tree.un_chomsky_normal_form()

        return lexicalize(tree, sent)

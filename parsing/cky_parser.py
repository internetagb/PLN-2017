from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """

        n = len(sent)
        prods = self.grammar.productions()
        term_prods = []
        non_term = []
        for p in prods:
            if p.__len__() == 1:
                term_prods.append(p)
            else:
                prod = [str(p.lhs()), str(p.rhs()[0]), str(p.rhs()[1])]
                prod.append(p.logprob())
                non_term.append(prod)
        pi = defaultdict(dict)
        bp = dict()

        # base case
        for i in range(1, n+1):
            word = sent[i-1]
            for p in [t for t in term_prods if t.rhs()[0] == word]:
                term = str(p.lhs())
                pi[(i, i)][term] = p.logprob()
                bp[(i, i)] = defaultdict()
                bp[(i, i)][term] = Tree(term, [word])
        # recursive cases
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i+l
                # for X in N:
                #     for prod in [t for t in non_term if str(t.lhs()) == X]:
                bp[(i, j)] = defaultdict()
                for prod in non_term:
                    X, Y, Z, prob = prod
                    for s in range(i, j):
                        if Y in pi[(i, s)].keys() and Z in pi[(s+1, j)].keys():
                            prob += pi[(i, s)][Y] + pi[(s+1, j)][Z]
                            if X not in pi[(i, j)] or pi[(i, j)][X] < prob:
                                pi[(i, j)][X] = prob
                                tree = [bp[(i, s)][Y], bp[(s+1, j)][Z]]
                                bp[(i, j)][X] = Tree(X, tree)
        lp = pi[(1, n)].get('S', float('-inf'))
        t = bp[(1, n)].get('S', None)

        self._pi = dict(pi)
        self._bp = bp

        return lp, t

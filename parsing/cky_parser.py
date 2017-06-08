from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar
        self.start = str(grammar.start())
        prods = grammar.productions()
        term_prods = defaultdict(list)
        non_term = defaultdict(list)
        for p in prods:
            if p.__len__() == 1:
                term_prods[str(p.rhs()[0])].append((str(p.lhs()), p.logprob()))
            else:
                key = (str(p.rhs()[0]), str(p.rhs()[1]))
                non_term[key].append((str(p.lhs()), p.logprob()))
        self._tm = dict(term_prods)
        self._nt = dict(non_term)

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """

        n = len(sent)
        pi = {}
        bp = {}
        term_prods = self._tm
        non_term = self._nt

        # base case
        for i in range(1, n+1):
            leaf = sent[i-1]
            bp[(i, i)] = {}
            pi[(i, i)] = {}
            for p in term_prods[leaf]:
                term = p[0]
                pi[(i, i)][term] = p[1]
                bp[(i, i)][term] = Tree(term, [leaf])
        # recursive cases
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i+l
                pi[(i, j)] = {}
                bp[(i, j)] = {}
                for s in range(i, j):
                    for Y, lprobY in pi[(i, s)].items():
                        for Z, lprobZ in pi[(s+1, j)].items():
                            for X, lprobX in non_term.get((Y, Z), []):
                                lprob = lprobX + lprobY + lprobZ
                                if (X not in pi[(i, j)]
                                        or pi[(i, j)][X] < lprob):
                                    pi[(i, j)][X] = lprob
                                    tree = [bp[(i, s)][Y], bp[(s+1, j)][Z]]
                                    bp[(i, j)][X] = Tree(X, tree)
        lp = pi[(1, n)].get(self.start, float('-inf'))
        t = bp[(1, n)].get(self.start, None)

        self._pi = dict(pi)
        self._bp = bp

        return lp, t

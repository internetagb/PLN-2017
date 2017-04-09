# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log

def ngram_delim(n, sent):
    sent = ['<s>']*(n-1) + sent + ['</s>']
    return sent

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            sent = ngram_delim(n, sent)
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
             prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]

        p1 = self.counts[tuple(tokens)]
        p2 = self.counts[tuple(prev_tokens)]

        prob = 0

        if p2 != 0:
            prob = float(p1)/p2

        return prob


    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        prob = 1
        sent = ngram_delim(n, sent)

        for i in range(n-1, len(sent)):
            prev_tokens = sent[i-n+1:i]
            token = sent[i]
            prob *= self.cond_prob(token, prev_tokens)

        return prob


    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """
        log2 = lambda x: log(x, 2)
        n = self.n
        prob = 0
        sent = ngram_delim(n, sent)

        for i in range(n-1, len(sent)):
            prev_tokens = sent[i-n+1:i]
            token = sent[i]
            prob_temp = self.cond_prob(token, prev_tokens)
            if prob_temp == 0:
                prob = float('-inf')
            else:
                prob += log2(prob_temp)

        return prob
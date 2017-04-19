# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random


def ngram_delim(n, sent):
    """Add delimiters at the beginning and at the end of the sentence.
    n -- order of the model.
    sent -- one sentence (a list of tokens).
    """
    sent = ['<s>']*(n-1) + sent + ['</s>']
    return sent


def log2(x):
    """Calculate log (base 2) of x.
    """
    return log(x, 2)


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        # add delimiters to each sentence and build n-grams
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
        # n = self.n
        if not prev_tokens:
            prev_tokens = []
        # assert len(prev_tokens) == n - 1    # check n-gram size

        tokens = prev_tokens + [token]

        p1 = self.counts[tuple(tokens)]    # appearances of (prev_tokens,token)
        p2 = self.counts[tuple(prev_tokens)]    # appearances of prev_tokens

        prob = 0

        if p2 != 0:
            # calculate probability P(token | prev_tokens) using counts.
            prob = float(p1)/p2

        return prob

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        prob = 1
        sent = ngram_delim(n, sent)
        # for each n-gram of the sentece,
        # calculate the conditional probability using Markov Assumption.
        for i in range(n-1, len(sent)):
            prev_tokens = sent[i-n+1:i]
            token = sent[i]
            prob *= self.cond_prob(token, prev_tokens)

        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        prob = 0
        sent = ngram_delim(n, sent)
        # calculate log(base 2) of conditional probability
        # of each n-gram related to the sentence.
        for i in range(n-1, len(sent)):
            prev_tokens = sent[i-n+1:i]
            token = sent[i]
            prob_temp = self.cond_prob(token, prev_tokens)
            if prob_temp == 0:
                prob = float('-inf')
            else:
                # calculate log base 2.
                # Domain error is not a problem (because 'if statement').
                prob += log2(prob_temp)

        return prob

    def log_probability(self, sents):
        """Log-probability of sentences.
        sents -- list of sentences, each one being a list of tokens.
        """
        log_prob = sum(self.sent_log_prob(sent) for sent in sents)

        return log_prob

    def cross_entropy(self, sents):
        """Cross-entropy of sentences.
        sents -- list of sentences, each one being a list of tokens.
        """
        M = sum([len(sent) for sent in sents])
        log_probability = self.log_probability(sents)

        cross_entropy = log_probability / float(M)

        return cross_entropy

    def perplexity(self, sents):
        """Perplexity of sentences.
        sents -- list of sentences, each one being a list of tokens.
        """
        l = self.cross_entropy(sents)

        perplexity = 2**(-l)

        return perplexity


class NGramGenerator:

    def __init__(self, model):
        """
        model -- n-gram model.
        """

        # create structures
        self.probs = probs = defaultdict(dict)
        self.sorted_probs = sorted_probs = defaultdict(dict)
        self.n = n = model.n
        counts = model.counts
        # initialize structures
        for words in counts.keys():
            if len(words) == n:
                token = words[n-1]
                prev_tokens = words[:n-1]
                if prev_tokens not in probs:
                    probs.update({prev_tokens: defaultdict(dict)})
                    sorted_probs.update({prev_tokens: []})
                current_prob = model.cond_prob(token, list(prev_tokens))
                probs[prev_tokens].update({token: current_prob})
                sorted_probs[prev_tokens].append((token, current_prob))
                sorted_probs[prev_tokens] = sorted(sorted_probs[prev_tokens],
                                                   key=lambda x: (-x[1], x[0]))

    def generate_sent(self):
        """Randomly generate a sentence."""
        n = self.n

        sent = prev_tokens = ['<s>'] * (n-1)    # add initial delimiters
        end_delim = '</s>'
        new_token = ''

        # while not end of sentence, generate a new token
        while new_token != end_delim:
            new_token = self.generate_token(tuple(prev_tokens))
            sent.append(new_token)
            prev_tokens = tuple(sent[len(sent)-n+1:])

        return sent[n-1:len(sent)-1]

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            prev_tokens = ()

        tokens = self.sorted_probs[prev_tokens]
        prob = 0
        X = random()
        gen_token = ''
        i = 0

        # choose token using inverse transform sampling
        while prob < X:
            gen_token, prob_token = tokens[i]
            prob += prob_token
            i += 1

        return gen_token


class AddOneNGram(NGram):

    def __init__(self, n, sents):

        super().__init__(n, sents)

        word_types = set(word for sent in sents for word in sent)
        # add 1 because of "end of sentece"('</s>') delimiter.
        self.vocabulary_size = len(word_types) + 1

    def V(self):
        """Size of the vocabulary.
        """
        return self.vocabulary_size

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1    # check n-gram size

        tokens = prev_tokens + [token]
        # appearances of (prev_tokens,tokens), plus one (addOne).
        p1 = float(self.counts[tuple(tokens)]) + 1
        # appearances of prev_tokens plus vocabulary size.
        p2 = self.counts[tuple(prev_tokens)] + self.V()

        prob = 0

        if p2 != 0:
            # calculate probability
            # (c(prev_token,token) + 1) / (c(prev_token) + V)
            prob = float(p1)/p2

        return prob


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.counts = counts = defaultdict(int)
        words_count = len(sents)
        self.gamma = gamma

        for sent in sents:
            words_count += len(sent)
            for k in range(1, n+1):
                sent_tmp = ngram_delim(k, sent)
                for i in range(len(sent_tmp) - k + 1):
                    ngram = tuple(sent_tmp[i: i + k])
                    counts[ngram] += 1
        counts[()] = words_count

    def lambdas(self, tokens, lambda_list):

        gamma = self.gamma
        tokens = tuple(tokens)
        count = self.counts[tokens]
        print(tokens)
        print(count)
        print(sum(lambda_list))
        lambd = (1-sum(lambda_list))

        if tokens:
            lambd *= (count/(count+gamma))

        return lambd

    def cond_prob(self, token, prev_tokens=None):

        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1    # check n-gram size
        lambda_list = []
        probs = []
        prob = 0

        if n == 1:
            prob = super().cond_prob(token)

        for i in range(n):
            prev_tokens = prev_tokens[i:]
            lambd = self.lambdas(prev_tokens, lambda_list)
            lambda_list.append(lambd)
            MLprob = super().cond_prob(token, prev_tokens)
            current_prob = lambda_list[i] * MLprob
            probs.append(current_prob)

        prob = sum(probs)

        return prob

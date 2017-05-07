from math import log2


class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tagset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        return self.trans.get(prev_tags, {}).get(tag, 0.0)

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        return self.out.get(tag, {}).get(word, 0.0)

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- tagging.
        """
        prob = 1.0
        n = self.n
        y_tmp = ['<s>']*(n-1) + y + ['</s>']

        while len(y_tmp) > n-1 and prob is not 0.0:
            prob *= self.trans_prob(y_tmp[n-1], tuple(y_tmp[:n-1]))
            y_tmp = y_tmp[1:]

        return prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        i = 0
        e = 1.0
        q = self.tag_prob(y)
        while i < len(x) and e is not 0.0:
            e *= self.out_prob(x[i], y[i])
            i += 1

        return q*e

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        prob = 0.0
        n = self.n
        y_tmp = ['<s>']*(n-1) + y + ['</s>']

        while len(y_tmp) > n-1 and prob is not float('-inf'):
            prob_tmp = self.trans_prob(y_tmp[n-1], tuple(y_tmp[:n-1]))
            if prob_tmp is 0.0:
                prob = float('-inf')
            else:
                prob += log2(prob_tmp)

            y_tmp = y_tmp[1:]

        return prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """
        i = 0
        prob = self.tag_log_prob(y)
        while i < len(x) and prob is not float('-inf'):
            e = self.out_prob(x[i], y[i])
            if e is 0.0:
                prob = float('-inf')
            else:
                prob += log2(e)
            i += 1

        return prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """

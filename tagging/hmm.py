from math import log2
from collections import defaultdict


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
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        hmm = self.hmm
        self._pi = pi = defaultdict(defaultdict)
        pi[0][('<s>',)*(hmm.n-1)] = (0.0, [])

        for k in range(1, len(sent)+1):
            for v in hmm.tagset:
                for prev_tags, (prob, tags) in pi[k-1].items():
                    e = hmm.out_prob(sent[k-1], v)
                    q = hmm.trans_prob(v, prev_tags)
                    if q*e > 0.0:
                        prob += log2(q) + log2(e)
                        prev_tags = (prev_tags + (v,))[1:]
                        if (prev_tags not in pi[k-1] or
                                prob > pi[k-1][prev_tags][0]):
                            pi[k][prev_tags] = (prob, tags + [v])

        final_tags = []
        max_prob = float('-inf')
        for prev_tags, (prob, tags) in pi[len(sent)].items():
            q = hmm.trans_prob('</s>', prev_tags)
            if q > 0.0:
                prob += log2(q)
                if prob > max_prob:
                    max_prob = prob
                    final_tags = tags

        return final_tags


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.addone = addone
        self.counts = counts = defaultdict(int)
        k_words = set()
        tagset = set()
        trans = defaultdict(lambda: defaultdict(float))
        out = defaultdict(lambda: defaultdict(float))

        # initialize n-grams (of tags) count
        for sent in tagged_sents:
            words, tags = zip(*sent)
            k_words = k_words.union(words)
            tagset = tagset.union(tags)
            tags = ('<s>',)*(n-1) + tags + ('</s>',)
            words = ('<s>',)*(n-1) + words + ('</s>',)
            for i in range(len(tags) - n + 1):
                ngram = tuple(tags[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
                out[tags[i]][words[i]] += 1

        # store known words and possible tags
        self.tagset = tagset
        self.known_words = k_words

        # calculate trans probs
        for ng in [ngram for ngram in counts if len(ngram) == n]:
            c1 = counts[ng]
            c2 = counts[ng[:-1]]
            if addone:
                c1 += 1
                c2 += len(k_words) + 1
            trans[ng[:-1]][ng[-1]] = float(c1)/c2
        self.trans = dict(trans)

        # calculate out probs
        for dict_value in out.values():
            total = sum(dict_value.values())
            for key, value in dict_value.items():
                dict_value[key] = value/total
        self.out = dict(out)

    def tcount(self, tokens):
        """Count for an n-gram or (n-1)-gram of tags.

        tokens -- the n-gram or (n-1)-gram tuple of tags.
        """
        return self.counts.get(tokens, 0)

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return w not in self.known_words

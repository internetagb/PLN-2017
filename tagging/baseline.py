from collections import Counter, defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        self.word_tag = word_tag = {}
        wt_tmp = defaultdict(list)

        for tagged_sent in tagged_sents:
            for word, tag in tagged_sent:
                wt_tmp[word].append(tag)

        for word in wt_tmp:
            word_tag[word] = Counter(wt_tmp.get(word)).most_common(1)[0][0]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        return self.word_tag.get(w, 'nc0s000')

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return (w not in self.word_tag)

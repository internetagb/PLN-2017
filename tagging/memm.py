from tagging.features import History


class MEMM:

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        k_words = set()
        for sent in tagged_sents:
            k_words = k_words.union([word for (word, _) in sent])
        self.known_words = k_words

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        return [h for sent in tagged_sents for h in self.sent_histories(sent)]

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        result = []
        sent = []
        tags = ['<s>']*(n-1)
        for word, tag in tagged_sent:
            sent.append(word)
            tags.append(tag)
        for i in range(len(tagged_sent)):
            prev_tags = tuple(tags[i+j] for j in range(n-1))
            result.append(History(sent, prev_tags, i))
        return result

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        return [tag for sent in tagged_sents for tag in self.sent_tags(sent)]

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        return [tag for _, tag in tagged_sent]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """

    def tag_history(self, h):
        """Tag a history.

        h -- the history.
        """

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return w not in self.known_words

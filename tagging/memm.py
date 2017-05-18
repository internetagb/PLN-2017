from tagging.features import (History, word_lower, word_istitle, word_isupper,
                              word_isdigit, NPrevTags, PrevWord)
from sklearn.pipeline import Pipeline
from featureforge.vectorizer import Vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


class MEMM:

    def __init__(self, n, tagged_sents, clf='lr'):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.known_words = set([p[0] for sent in tagged_sents for p in sent])
        features = [word_lower, word_istitle, word_isupper, word_isdigit]
        features += [PrevWord(f) for f in features]
        features += [NPrevTags(i) for i in range(1, n)]
        if clf == 'mnb':
            classifier = MultinomialNB()
        elif clf == 'svc':
            classifier = LinearSVC()
        else:
            classifier = LogisticRegression()
        pline = Pipeline([('vect', Vectorizer(features)),
                          ('clf', classifier)])
        histories = self.sents_histories(tagged_sents)
        tags = self.sents_tags(tagged_sents)
        pline.fit(histories, tags)
        self.pipeline = pline

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
        # print(tagged_sent)
        for word, tag in tagged_sent:
            sent.append(word)
            tags.append(tag)
        for i in range(len(tagged_sent)):
            prev_tags = tuple(tags[i:i+n-1])
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
        prev_tags = ('<s>',)*(self.n-1)
        tags = [self.tag_history(History(sent, prev_tags, 0))]
        for i in range(1, len(sent)):
            prev_tags = (prev_tags + (tags[i-1],))[1:]
            tags.append(self.tag_history(History(sent, prev_tags, i)))

        return tags

    def tag_history(self, h):
        """Tag a history.

        h -- the history.
        """
        return self.pipeline.predict([h])[0]

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return w not in self.known_words

from collections import namedtuple
from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()


def prev_tags(h):
    """Return prevoius tags of a history

    h -- a history.
    """
    return h.prev_tags


def word_istitle(h):
    """Feature: current word is title.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()


def word_isupper(h):
    """Feature: current uppercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()


def word_isdigit(h):
    """Feature: current word is a digit.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()


class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """
        self.n = n

    def _evaluate(self, h):
        """n previous tags tuple.

        h -- a history.
        """
        return prev_tags(h)[-self.n:]


class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.

        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.

        h -- the history.
        """
        if h.i is 0:
            return 'BOS'
        else:
            return str(self.f(History(h.sent, prev_tags(h), (h.i)-1)))

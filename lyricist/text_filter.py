import collections
from abc import ABCMeta, abstractmethod

class TextFilter(object, metaclass=ABCMeta):
    """ An intertface for text filters 

        Only has one method: apply() which recieves a string as 
        an argument and returns a string. 
    """

    @abstractmethod
    def apply(self, text):
        """ Recieves a string, filters it, and returns a string. """
        pass

class Pipeline(object):
    """ A composite TextFilter class 

        Uses the Composite Pattern with TextFilters
    """

    def __init__(self, filters=None):
        self._filters = []

        if filters is not None:
            # if a single filter was provided, turn it into a list
            if not isinstance(filters, collections.Iterable):
                filters = [filters]
                
            for fil in filters:
                self.add(fil)

    def add(self, fil):
        if isinstance(filter, TextFilter):
            raise TypeError("fil must be a subclass of TextFilter")
        self._filters += [fil]
        return self # allow chained additions

    def apply(self, string):
        result = string
        for fil in self._filters:
            result = fil.apply(result)
        return result

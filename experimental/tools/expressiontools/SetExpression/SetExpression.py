import abc
from abjad.tools import timespantools
from experimental.tools.expressiontools.Expression import Expression


class SetExpression(Expression):
    '''Set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    #def __init__(self, attribute=None, source=None, target_timespan=None):
    def __init__(self, source=None, target_timespan=None):
        from experimental.tools import expressiontools
        #assert isinstance(attribute, str), repr(attribute)
        assert isinstance(source, expressiontools.Expression), repr(source)
        assert isinstance(target_timespan, (timespantools.Timespan, expressiontools.TimespanExpression, 
            str, type(None))), repr(target_timespan)
        #self._attribute = attribute
        self._source = source
        self._target_timespan = target_timespan
        self._lexical_rank = None

    ### READ-ONLY PUBLIC PROPERTIES ###

#    @property
#    def attribute(self):
#        return self._attribute

    @property
    def source(self):
        return self._source

    @property
    def target_timespan(self):
        return self._target_timespan

# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.SetExpression \
    import SetExpression


class TimespanScopedSingleContextSetExpression(SetExpression):
    r'''Timespan-scoped single-context set expression.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, 
        attribute=None, 
        source_expression=None, 
        target_timespan=None, 
        target_context_name=None,
        fresh=None,
        ):
        assert isinstance(target_context_name, (str, type(None)))
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        SetExpression.__init__(
            self, 
            attribute=attribute, 
            source_expression=source_expression, 
            target_timespan=target_timespan,
            )
        self._target_context_name = target_context_name
        self._fresh = fresh

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when `expr` is a timespan-scoped single-context set expression
        with same source_expression, target timespan and target context name.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_expression == expr.source_expression and \
                self.target_timespan == expr.target_timespan and \
                self.target_context_name == expr.target_context_name:
                return True
        return False

    def __lt__(self, expr):
        r'''True when timespan-scoped single-context set expression 
        target timespan is less than `expr` target_timespan.
        Otherwise false.

        Returns boolean.
        '''
        if self.target_timespan.starts_before_timespan_starts(expr):
            return True
        elif self.target_timespan.starts_when_timespan_starts(expr):
            return self.target_timespan.stops_before_timespan_stops(expr)
        return False

    def __or__(self, set_expression):
        r'''Logical OR of timespan-scoped single-context set expression 
        and `set_expression`.

        Raises exception when timespan-scoped single-context set expression 
        can not fuse with `set_expression`.

        Returns timespan inventory.
        '''
        assert self._can_fuse(set_expression)
        stop_offset = self.target_timespan.stop_offset + \
            set_expression.target_timespan.duration
        target_timespan = self.target_timespan.new(stop_offset=stop_offset)
        result = self.new(target_timespan=target_timespan)
        return timespantools.TimespanInventory([result])

    def __sub__(self, timespan):
        r'''Subtract `timespan` from timespan-scoped single-context 
        set expression.

        Operates in place and returns timespan-scoped single-context 
        set expression inventory.
        '''
        from experimental.tools import musicexpressiontools
        timespans = self.target_timespan - timespan
        result = \
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for timespan in timespans:
            region_expression = self.new(target_timespan=timespan)
            result.append(region_expression)
        return result

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _can_fuse(self, expr):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        r'''True when set expression was generated in response
        to explicit user input. Otherwise false.

        Returns boolean.
        '''
        return self._fresh

    # TODO: remove and use self.timespan.start_offset instead
    @property
    def start_offset(self):
        r'''Set expression start offset.

        .. note:: remove and use ``self.timespan.start_offset`` instead.

        Returns offset.
        '''
        return self.target_timespan.start_offset

    # TODO: remove and use self.timespan.stop_offset instead
    @property
    def stop_offset(self):
        r'''Set expression stop offset.

        .. note:: remove and use ``self.timespan.stop_offset`` instead.

        Returns offset.
        '''
        return self.target_timespan.stop_offset

    @property
    def target_context_name(self):
        r'''Set expression context name.

        Returns string.
        '''
        return self._target_context_name

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        r'''Evaluate timespan-scoped single-context set expression.

        Returns region expression.
        '''
        pass
# -*- encoding: utf-8 -*-
import copy
from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.TimespanScopedSingleContextSetExpression \
    import TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextDivisionSetExpression(
    TimespanScopedSingleContextSetExpression):
    r'''Timespan-delimited single-context division set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        source_expression=None, 
        target_timespan=None, 
        scope_name=None,
        fresh=None, 
        truncate=None,
        ):
        TimespanScopedSingleContextSetExpression.__init__(
            self, 
            attribute='divisions',
            source_expression=source_expression, 
            target_timespan=target_timespan,
            scope_name=scope_name, 
            fresh=fresh,
            )
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if self.truncate:
            return False
        if expr.fresh or expr.truncate:
            return False
        if expr.source_expression != self.source_expression:
            return False
        if not self.target_timespan.stops_when_timespan_starts(
            expr.target_timespan):
            return False
        return True

    ## PUBLIC PROPERTIES ###

    @property
    def truncate(self):
        r'''Is true when timespan-delimited single-context division set expression
        should truncate at segment boundaries.
        Otherwise false.

        Returns boolean.
        '''
        return self._truncate

    @property
    def voice_name(self):
        r'''Aliased to `scope_name`.

        Returns string.
        '''
        return self.scope_name

    ### PUBLIC METHODS ###

    def evaluate(self, voice_name):
        r'''Evaluate timespan-delimited single-context division set expression.

        Returns division region expression.
        '''
        from experimental.tools import musicexpressiontools
        start_offset = self.target_timespan.start_offset
        total_duration = self.target_timespan.duration
        if isinstance(
            self.source_expression, musicexpressiontools.SelectExpression):
            region_expression = \
                musicexpressiontools.SelectExpressionDivisionRegionExpression(
                self.source_expression, 
                start_offset, 
                total_duration, 
                voice_name,
                )
        elif isinstance(
            self.source_expression, 
            musicexpressiontools.DivisionSetExpressionLookupExpression):
            expression = self.source_expression.evaluate()
            assert isinstance(
                expression, musicexpressiontools.IterablePayloadExpression)
            divisions = expression.elements
            region_expression = \
                musicexpressiontools.LiteralDivisionRegionExpression(
                divisions, 
                start_offset, 
                total_duration, 
                voice_name,
                )
        elif isinstance(
            self.source_expression, 
            musicexpressiontools.IterablePayloadExpression):
            divisions = self.source_expression.elements
            region_expression = \
                musicexpressiontools.LiteralDivisionRegionExpression(
                divisions, 
                start_offset, 
                total_duration, 
                voice_name,
                )
        else:
            raise TypeError(self.source_expression)
        return region_expression

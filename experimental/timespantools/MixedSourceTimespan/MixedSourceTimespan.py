from abjad.tools import abctools
from experimental.timespantools.Timespan import Timespan


class MixedSourceTimespan(Timespan):
    r'''.. versionadded:: 1.0

    Mixed-source timespan.

        >>> from experimental import *

    Mixed-source timespan starting at the left edge of the last measure in the segment 
    with name ``'red'`` and stopping at the right edge of the first measure in the segment 
    with name ``'blue'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> inequality = timespaninequalitytools.expr_2_starts_during_expr_1(expr_1=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSelector(inequality=inequality, start_identifier=-1)
        >>> start_timepoint = timespantools.Timepoint(anchor=measure_selector)

    ::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='blue')
        >>> inequality = timespaninequalitytools.expr_2_starts_during_expr_1(expr_1=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSelector(inequality=inequality, stop_identifier=1)
        >>> stop_timepoint = timespantools.Timepoint(anchor=measure_selector, edge=Right)
        
    ::

        >>> timespan = timespantools.MixedSourceTimespan(
        ... start_timepoint=start_timepoint, stop_timepoint=stop_timepoint)

    ::

        >>> z(timespan)
        timespantools.MixedSourceTimespan(
            start_timepoint=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureSelector(
                    inequality=timespaninequalitytools.TimespanInequality(
                        'expr_1.start <= expr_2.start < expr_1.stop',
                        expr_1=timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='red'
                                )
                            )
                        ),
                    start_identifier=-1
                    )
                ),
            stop_timepoint=timespantools.Timepoint(
                anchor=selectortools.BackgroundMeasureSelector(
                    inequality=timespaninequalitytools.TimespanInequality(
                        'expr_1.start <= expr_2.start < expr_1.stop',
                        expr_1=timespantools.SingleSourceTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='blue'
                                )
                            )
                        ),
                    stop_identifier=1
                    ),
                edge=Right
                )
            )

    Mixed-source timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start_timepoint=None, stop_timepoint=None):
        from experimental import timespantools
        assert isinstance(start_timepoint, (timespantools.Timepoint, type(None))), repr(start_timepoint)
        assert isinstance(stop_timepoint, (timespantools.Timepoint, type(None))), repr(stop_timepoint)
        Timespan.__init__(self)
        self._start_timepoint = start_timepoint
        self._stop_timepoint = stop_timepoint

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isintance(expr, type(self)):
            if self.start_timepoint == expr_2.start_timepoint:
                if self.stop_timepoint == expr_2.stop_timepoint:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_anchored_to_one_object(self):
        '''True when start anchor equals stop anchor. Otherwise false.

        Return boolean.
        '''
        return self.start_timepoint.anchor == self.stop_timepoint.anchor


    def encompasses_one_object_exactly(self):
        '''True when the following five conditions hold:

        1. start anchor equals stop anchor.

        2. start edge is left.

        3. stop edge is right.

        4. start and stop multipliers are both none.
    
        5. start and stop addenda are both none.

        Return boolean.
        '''
        if self.start_timepoint.anchor == self.stop_timepoint.anchor:
            if self.start_timepoint.edge in (None, Left):
                if self.stop_timepoint.edge == Right:
                    if self.start_timepoint.multiplier is self.stop_timepoint.multiplier is None:
                        if self.start_timepoint.addendum is self.stop_timepoint.addendum is None:
                            return True
        return False

    @property
    def encompasses_one_segment_exactly(self):
        '''False.
        '''
        return False


    @property
    def start_timepoint(self):
        '''Mixed-source timespan start timepoint specified by user.

        Return timepoint or none.
        '''
        return self._start_timepoint

    @property
    def stop_timepoint(self):
        '''Mixed-source timepsan stop timepoint specified by user.

        Return timepoint or none.
        '''
        return self._stop_timepoint

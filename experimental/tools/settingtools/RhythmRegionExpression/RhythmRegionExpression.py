import copy
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.RegionExpression import RegionExpression


class RhythmRegionExpression(RegionExpression):
    r'''Rhythm region command.

    Region command indicating durated period of time 
    over which a rhythm-maker will apply.
    '''

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region command.

            >>> expression = settingtools.PayloadExpression("{ c'16 [ c'8 ] }")
            >>> timespan = timespantools.Timespan(0, 20)
            >>> rhythm_region_command = settingtools.RhythmRegionExpression(
            ...     expression, 'Voice 1', timespan)

        ::

            >>> result = rhythm_region_command - timespantools.Timespan(5, 15)

        ::

            >>> z(result)
            settingtools.RegionExpressionInventory([
                settingtools.RhythmRegionExpression(
                    expression=settingtools.PayloadExpression(
                        "{ c'16 [ c'8 ] }"
                        ),
                    context_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1)
                        )
                    ),
                settingtools.RhythmRegionExpression(
                    expression=settingtools.PayloadExpression(
                        "{ c'16 [ c'8 ] }"
                        ),
                    context_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1)
                        )
                    )
                ])

        Return region command inventory.
        '''
        return RegionExpression.__sub__(self, timespan)
    
    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if expr.fresh:
            return False
        if expr.expression != self.expression:
            return False
        return True

    # TODO: maybe make RhythmRegionExpression abstract and make this method abstract
    def _evaluate(self):
        raise NotImplemented

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'rhythm'

    ### PUBLIC METHODS ###

    # TODO: maybe implement finalize() methods on PayloadExpression, RhythmMakerPayloadExpression, etc.
    def finalize(self, score_specification, voice_name, start_offset, division_list):
        from experimental.tools import selectortools
        from experimental.tools import settingtools
        assert isinstance(start_offset, durationtools.Offset), repr(start_offset)
        assert isinstance(division_list, settingtools.DivisionList), repr(division_list)
        assert isinstance(voice_name, str), repr(voice_name)
        if isinstance(self.expression, settingtools.RhythmMakerPayloadExpression):
            rhythm_maker = self.expression.payload
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            command = settingtools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, voice_name, start_offset, division_list)
        # TODO: change the test of this branch to test for something like ParseableStringPayloadExpression
        #       or perhaps even ScoreComponentPayloadExpression, either of which will have to be newly implemented
        elif isinstance(self.expression, settingtools.PayloadExpression):
            parseable_string = self.expression.payload
            assert isinstance(parseable_string, str), repr(parseable_string)
            command = settingtools.ParseableStringRhythmRegionExpression(
                parseable_string, voice_name, start_offset, division_list.duration)
        elif isinstance(self.expression, settingtools.RhythmSettingLookup):
            rhythm_maker = self.expression._evaluate(score_specification)
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            command = settingtools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, voice_name, start_offset, division_list)
        elif isinstance(self.expression, selectortools.CounttimeComponentSelector):
            total_duration = self.timespan.duration
            command_start_offset = self.timespan.start_offset
            command = settingtools.SelectorRhythmRegionExpression(
                self.expression, voice_name, command_start_offset, total_duration)
        else:
            raise TypeError(self.expression)
        return command

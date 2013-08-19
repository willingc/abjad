# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.CounterpointInterval import CounterpointInterval
from abjad.tools.pitchtools.MelodicInterval import MelodicInterval


class MelodicCounterpointInterval(CounterpointInterval, MelodicInterval):
    '''Abjad model of melodic counterpoint interval:

    ::

        >>> pitchtools.MelodicCounterpointInterval(-9)
        MelodicCounterpointInterval(-9)

    Melodic counterpoint intervals are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, number):
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero integer.')
        if abs(number) == 1:
            number = 1
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self._direction_symbol, abs(self.number))

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic counterpoint interval `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.MelodicCounterpointInterval.from_pitch_carriers(
            ...     pitchtools.NamedChromaticPitch(-2), 
            ...     pitchtools.NamedChromaticPitch(12),
            ...     )
            MelodicCounterpointInterval(+9)

        Return melodic counterpoint interval.
        '''
        from abjad.tools import pitchtools
        # get melodic diatonic interval
        mdi = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return melodic counterpoint interval
        return mdi.melodic_counterpoint_interval

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        if self.number < 0:
            return -1
        elif self.number == 1:
            return 0
        elif 1 < self.number:
            return 1
        else:
            raise ValueError

    @property
    def melodic_counterpoint_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.MelodicCounterpointIntervalClass(self)

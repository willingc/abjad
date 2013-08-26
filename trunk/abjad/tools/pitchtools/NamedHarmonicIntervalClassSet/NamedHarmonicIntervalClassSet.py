# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.IntervalClassSet import IntervalClassSet


class NamedHarmonicIntervalClassSet(IntervalClassSet):
    '''Abjad model of harmonic diatonic interval-class set:

    ::

        >>> pitchtools.NamedHarmonicIntervalClassSet('m2 M2 m3 M3') # doctest: +SKIP
        NamedHarmonicIntervalClassSet('m2 M2 m3 M3')

    Harmonic diatonic interval-class sets are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, str):
            interval_tokens = arg.split()
        else:
            interval_tokens = arg
        hdics = [pitchtools.NamedHarmonicIntervalClass(x) 
            for x in interval_tokens]
        return frozenset.__new__(self, hdics)

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __repr__(self):
        return "%s('%s')" % (self._class_name, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ' '.join([str(x) for x in 
            sorted(self.harmonic_diatonic_interval_classes)])

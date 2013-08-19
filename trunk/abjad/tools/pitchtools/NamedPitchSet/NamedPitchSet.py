# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Set import Set


class NamedPitchSet(Set):
    '''Abjad model of a named chromatic pitch set:

    ::

        >>> pitchtools.NamedPitchSet(
        ...     ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])
        NamedPitchSet(['bf', 'bqf', "fs'", "g'"])

    Named chromatic pitch sets are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __new__(cls, pitchs):
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        pitches = []
        for pitch in pitchs:
            if isinstance(pitch, notetools.NoteHead):
                pitch = pitchtools.NamedPitch(pitch.written_pitch)
                pitches.append(pitch)
            else:
                pitch = pitchtools.NamedPitch(pitch)
                pitches.append(pitch)
        return frozenset.__new__(cls, pitches)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            for element in arg:
                if element not in self:
                    return False
            else:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '{%s}' % ' '.join([str(pitch) 
            for pitch in self.named_chromatic_pitches])

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(pitch) for pitch in self.pitches])

    @property
    def _repr_string(self):
        return ', '.join([repr(str(pitch)) 
            for pitch in self.named_chromatic_pitches])

    ### PUBLIC PROPERTIES ###

    @property
    #def numbers(self):
    def chromatic_pitch_numbers(self):
        return tuple(sorted([
            pitch.numbered_chromatic_pitch._chromatic_pitch_number 
            for pitch in self]))

    @property
    def duplicate_pitch_classes(self):
        from abjad.tools import pitchtools
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = pitch.numbered_chromatic_pitch_class
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return pitchtools.NumberedPitchClassSet(
            duplicate_pitch_classes)

    @property
    def is_pitch_class_unique(self):
        return len(self) == len(self.numbered_chromatic_pitch_class_set)

    @property
    #def pitches(self):
    def named_chromatic_pitches(self):
        return tuple(sorted(self))

    @property
    #def pitch_class_set(self):
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSet(self)

    @property
    #def pitch_classes(self):
    def numbered_chromatic_pitch_classes(self):
        return tuple([pitch.numbered_chromatic_pitch_class 
            for pitch in self.pitches])

    ### PUBLIC METHODS ###

    # TODO: Implement pitch set (axis) inversion.

    #def invert(self):
    #    r'''Transpose all pcs in self by n.'''
    #    return PCSet([pc.invert() for pc in self])

    def transpose(self, n):
        r'''Transpose all pcs in self by n.
        '''
        from abjad.tools import pitchtools
        interval = pitchtools.MelodicChromaticInterval(n)
        return type(self)([
            pitchtools.transpose_pitch_carrier_by_melodic_interval(
            pitch, interval) for pitch in self])
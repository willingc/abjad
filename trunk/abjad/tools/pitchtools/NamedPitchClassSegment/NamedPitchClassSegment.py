# -*- encoding: utf-8 -*-
import copy
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment


class NamedPitchClassSegment(PitchClassSegment):
    '''Abjad model of named chromatic pitch-class segment:

    ::

        >>> pitchtools.NamedPitchClassSegment(
        ...     ['gs', 'a', 'as', 'c', 'cs'])
        NamedPitchClassSegment(['gs', 'a', 'as', 'c', 'cs'])

    Named chromatic pitch-class segments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __new__(self, named_chromatic_pitch_class_tokens):
        from abjad.tools import pitchtools
        npcs = [pitchtools.NamedPitchClass(x) 
            for x in named_chromatic_pitch_class_tokens]
        return tuple.__new__(self, npcs)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    @property
    def _repr_string(self):
        return ', '.join([repr(str(x)) for x in self])

    ### PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_diatonic_interval_class_segment(self):
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        dics = mathtools.difference_series(self)
        return pitchtools.InversionEquivalentDiatonicIntervalClassSegment(dics)

    @property
    def named_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClassSet(self)

    @property
    def named_chromatic_pitch_classes(self):
        return tuple(self[:])

    @property
    def numbered_chromatic_pitch_class_segment(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSegment(self)

    @property
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSet(self)

    @property
    def numbered_chromatic_pitch_classes(self):
        return self.pitch_class_segment.pitch_classes

    ### PUBLIC METHODS ###

    def is_equivalent_under_transposition(self, arg):
        from abjad.tools import pitchtools
        if not isinstance(arg, type(self)):
            return False
        if not len(self) == len(arg):
            return False
        difference = -(pitchtools.NamedPitch(arg[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_npcs = [x + difference for x in self]
        new_npc_seg = type(self)(new_npcs)
        return arg == new_npc_seg

    def retrograde(self):
        return type(self)(reversed(self))

    def rotate(self, n):
        from abjad.tools import sequencetools
        named_chromatic_pitch_classes = sequencetools.rotate_sequence(
            self.named_chromatic_pitch_classes, n)
        return type(self)(named_chromatic_pitch_classes)

    def transpose(self, melodic_diatonic_interval):
        return type(self)([npc + melodic_diatonic_interval  for npc in self])
# -*- encoding: utf-8 -*-


def diatonic_pitch_name_to_pitch_name(diatonic_pitch_name):
    '''Change `diatonic_pitch_name` to chromatic pitch name:

    ::

        >>> pitchtools.diatonic_pitch_name_to_pitch_name("c''")
        "c''"

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.Pitch.is_diatonic_pitch_name(diatonic_pitch_name):
        raise TypeError

    return diatonic_pitch_name
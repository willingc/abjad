# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitch___init___01():
    r'''Init with number.
    '''

    assert isinstance(pitchtools.NumberedPitch(0), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(0.5), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(12), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(12.5), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(-12), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(-12.5), pitchtools.NumberedPitch)


def test_NumberedPitch___init___02():
    r'''Init with other numbered chromatic pitch instance.
    '''

    numbered_chromatic_pitch_1 = pitchtools.NumberedPitch(13)
    numbered_chromatic_pitch_2 = pitchtools.NumberedPitch(numbered_chromatic_pitch_1)

    assert isinstance(numbered_chromatic_pitch_1, pitchtools.NumberedPitch)
    assert isinstance(numbered_chromatic_pitch_2, pitchtools.NumberedPitch)
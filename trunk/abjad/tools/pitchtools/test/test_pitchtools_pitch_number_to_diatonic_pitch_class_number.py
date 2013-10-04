# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_number_to_diatonic_pitch_class_number_01():

    assert pitchtools.pitch_number_to_diatonic_pitch_class_number(11) == 6
    assert pitchtools.pitch_number_to_diatonic_pitch_class_number(12) == 0
    assert pitchtools.pitch_number_to_diatonic_pitch_class_number(13) == 0
    assert pitchtools.pitch_number_to_diatonic_pitch_class_number(14) == 1
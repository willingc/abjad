# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_named_pitch_class_01():

    pitch = pitchtools.NamedPitch('cs', 4)
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedPitchClass('cs')
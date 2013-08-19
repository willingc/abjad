# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitch___int___01():
    r'''Return chromatic pitch number of 12-ET numbered chromatic pitch as int.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedPitch(13)
    assert isinstance(int(numbered_chromatic_pitch), int)
    assert int(numbered_chromatic_pitch) == 13


def test_NumberedPitch___int___02():
    r'''Raise type error on non-12-ET numbered chromatic pitch.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedPitch(13.5)
    assert py.test.raises(TypeError, 'int(numbered_chromatic_pitch)')
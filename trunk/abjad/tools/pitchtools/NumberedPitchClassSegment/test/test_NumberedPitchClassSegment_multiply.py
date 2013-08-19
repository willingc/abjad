# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSegment_multiply_01():

    pcseg = pitchtools.NumberedPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedPitchClassSegment

    assert pcseg.multiply(0) == PCSeg([0, 0, 0, 0, 0, 0])
    assert pcseg.multiply(1) == PCSeg([0, 6, 10, 4, 9, 2])
    assert pcseg.multiply(5) == PCSeg([0, 6, 2, 8, 9, 10])
    assert pcseg.multiply(7) == PCSeg([0, 6, 10, 4, 3, 2])
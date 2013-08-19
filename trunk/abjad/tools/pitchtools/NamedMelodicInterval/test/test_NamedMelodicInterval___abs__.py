# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___abs___01():

    interval = pitchtools.NamedMelodicInterval('minor', 3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)


def test_NamedMelodicInterval___abs___02():

    interval = pitchtools.NamedMelodicInterval('minor', -3)
    assert abs(interval) == pitchtools.HarmonicDiatonicInterval('minor', 3)
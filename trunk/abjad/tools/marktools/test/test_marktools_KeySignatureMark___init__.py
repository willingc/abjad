# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_marktools_KeySignatureMark___init___01():
    r'''Initialize with pitch-class letter string and mode string.
    '''

    ks = marktools.KeySignatureMark('g', 'major')

    assert ks.tonic == pitchtools.NamedPitchClass('g')
    assert ks.mode == tonalanalysistools.Mode('major')
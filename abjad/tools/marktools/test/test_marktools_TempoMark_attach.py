# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_marktools_TempoMark_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    tempo = marktools.TempoMark((1, 8), 52)
    attach(tempo, score[0][0])

    tempo = marktools.TempoMark((1, 8), 52)
    assert pytest.raises(ExtraMarkError, 'attach(tempo, score[0][0])')
    assert pytest.raises(ExtraMarkError, 'attach(tempo, score[1][0])')
# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Marimba_sounding_pitch_of_written_middle_c_01():

    marimba = instrumenttools.Marimba()

    assert marimba.sounding_pitch_of_written_middle_c == "c'"
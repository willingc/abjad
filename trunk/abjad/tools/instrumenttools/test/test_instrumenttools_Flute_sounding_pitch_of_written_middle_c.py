# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Flute_sounding_pitch_of_written_middle_c_01():

    flute = instrumenttools.Flute()

    assert flute.sounding_pitch_of_written_middle_c == "c'"
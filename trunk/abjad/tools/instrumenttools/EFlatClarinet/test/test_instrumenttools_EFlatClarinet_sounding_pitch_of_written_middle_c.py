# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_EFlatClarinet_sounding_pitch_of_written_middle_c_01():

    e_flat_clarinet = instrumenttools.EFlatClarinet()

    assert e_flat_clarinet.sounding_pitch_of_written_middle_c == "ef'"
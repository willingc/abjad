from abjad import *


def test_Instrument_list_secondary_instruments_01():

    secondary_instruments = \
        instrumenttools.Instrument.list_secondary_instruments()

    assert instrumenttools.AltoFlute in secondary_instruments
    assert instrumenttools.BassClarinet in secondary_instruments
    assert instrumenttools.EnglishHorn in secondary_instruments
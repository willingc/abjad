# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Note_sounding_pitch_01():


    staff = Staff("d''8 e''8 f''8 g''8")
    piccolo = instrumenttools.Piccolo()
    attach(piccolo, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    assert staff[0].sounding_pitch == "d''"
    assert staff[1].sounding_pitch == "e''"
    assert staff[2].sounding_pitch == "f''"
    assert staff[3].sounding_pitch == "g''"
# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_notetools_make_repeated_notes_from_time_signatures_01():
    r'''Make repeated notes from list of integer pairs.
    '''

    notes = notetools.make_repeated_notes_from_time_signatures([(2, 8), (3, 32)], pitch = "d''")
    assert len(notes) == 2

    notes = sequencetools.flatten_sequence(notes)
    staff = Staff(notes)

    r'''
    \new Staff {
        d''8
        d''8
        d''32
        d''32
        d''32
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            d''8
            d''8
            d''32
            d''32
            d''32
        }
        '''
        )
    assert inspect(staff).is_well_formed()

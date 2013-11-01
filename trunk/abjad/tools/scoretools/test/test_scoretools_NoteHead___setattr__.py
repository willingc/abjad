# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_NoteHead___setattr___01():
    r'''Slots constrain note head attributes.
    '''

    note_head = scoretools.NoteHead("cs''")

    assert py.test.raises(AttributeError, "note_head.foo = 'bar'")
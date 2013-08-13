# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_componenttools_all_are_logical_voice_contiguous_components_01():
    r'''Components that start at the same moment are bad.
    Even if components are all part of the same thread.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    voice.insert(2, Voice(notetools.make_repeated_notes(2)))
    Container(voice[:2])
    Container(voice[-2:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        \new Voice {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert not componenttools.all_are_logical_voice_contiguous_components(
        [voice, voice[0]])
    assert not componenttools.all_are_logical_voice_contiguous_components(
        voice[0:1] + voice[0][:])
    assert not componenttools.all_are_logical_voice_contiguous_components(
        voice[-1:] + voice[-1][:])


def test_componenttools_all_are_logical_voice_contiguous_components_02():
    r'''True for strictly contiguous leaves in same staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert componenttools.all_are_logical_voice_contiguous_components(staff[:])


def test_componenttools_all_are_logical_voice_contiguous_components_03():
    r'''True for orphan components when allow_orphans is True.
        False for orphan components when allow_orphans is False.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    assert componenttools.all_are_logical_voice_contiguous_components(notes)
    assert not componenttools.all_are_logical_voice_contiguous_components(notes, allow_orphans=False)


def test_componenttools_all_are_logical_voice_contiguous_components_04():
    r'''False for time reordered leaves in staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    assert not componenttools.all_are_logical_voice_contiguous_components(staff[2:] + staff[:2])


def test_componenttools_all_are_logical_voice_contiguous_components_05():
    r'''True for unincorporated component.
    '''

    assert componenttools.all_are_logical_voice_contiguous_components([Staff("c'8 d'8 e'8 f'8")])


def test_componenttools_all_are_logical_voice_contiguous_components_06():
    r'''True for empty list.
    '''

    assert componenttools.all_are_logical_voice_contiguous_components([])


def test_componenttools_all_are_logical_voice_contiguous_components_07():
    r'''False when components belonging to same thread are ommitted.
    '''

    voice = Voice("c'8 d'8 e'8 f'8 g'8 a'8")
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8
        g'8
        a'8 ]
    }
    '''

    assert not componenttools.all_are_logical_voice_contiguous_components(voice[:2] + voice[-2:])


def test_componenttools_all_are_logical_voice_contiguous_components_08():
    r'''False when components belonging to same thread are ommitted.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert not componenttools.all_are_logical_voice_contiguous_components(voice[:1] + voice[-1:])
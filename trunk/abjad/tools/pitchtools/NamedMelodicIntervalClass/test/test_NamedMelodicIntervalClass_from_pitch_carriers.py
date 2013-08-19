# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalClass_from_pitch_carriers_01():
    r'''Ascending intervals greater than an octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-3), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', 3)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-2), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('major', 2)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(-1), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', 2)


def test_NamedMelodicIntervalClass_from_pitch_carriers_02():
    r'''Ascending octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(0), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('perfect', 8)


def test_NamedMelodicIntervalClass_from_pitch_carriers_03():
    r'''Ascending intervals less than an octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(9), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', 3)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(10), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('major', 2)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(11), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', 2)


def test_NamedMelodicIntervalClass_from_pitch_carriers_04():
    r'''Unison.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(12))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('perfect', 1)


def test_NamedMelodicIntervalClass_from_pitch_carriers_05():
    r'''Descending intervals greater than an octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-3))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', -3)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-2))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('major', -2)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(-1))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', -2)


def test_NamedMelodicIntervalClass_from_pitch_carriers_06():
    r'''Descending octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(0))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('perfect', -8)


def test_NamedMelodicIntervalClass_from_pitch_carriers_07():
    r'''Descending intervals less than an octave.
    '''

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', -3)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(10))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('major', -2)

    mcpi = pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(11))
    assert mcpi == pitchtools.NamedMelodicIntervalClass('minor', -2)
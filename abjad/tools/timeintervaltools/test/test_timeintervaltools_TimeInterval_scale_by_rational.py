# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
import pytest


def test_timeintervaltools_TimeInterval_scale_by_rational_01():
    r'''TimeInterval.scale_by_rational returns a new TimeInterval instance unless offset is 1.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_by_rational(2)
    assert i1 != i2
    i2 = i1.scale_by_rational(1)
    assert i1 == i2


def test_timeintervaltools_TimeInterval_scale_by_rational_02():
    r'''TimeInterval duration can be scaled with ints.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_by_rational(2)
    assert i2.start_offset == 3
    assert i2.duration == 40


def test_timeintervaltools_TimeInterval_scale_by_rational_03():
    r'''TimeInterval duration can be scaled with Fractions.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_by_rational(Fraction(1, 2))
    assert i2.start_offset == 3
    assert i2.duration == 10


def test_timeintervaltools_TimeInterval_scale_by_rational_04():
    r'''TimeInterval duration cannot be scaled to zero.
    '''

    i1 = TimeInterval(3, 23)
    assert pytest.raises(AssertionError,
        'i1.scale_by_rational(0)')


def test_timeintervaltools_TimeInterval_scale_by_rational_05():
    r'''TimeInterval duration cannot be scaled with negatives.
    '''

    i1 = TimeInterval(3, 23)
    assert pytest.raises(AssertionError,
        'i2 = i1.scale_by_rational(-1)')
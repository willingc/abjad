# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval


def test_timeintervaltools_TimeInterval_signature_01():
    i = TimeInterval(0, 10, {'hello': 'world!'})
    assert i.signature == (0, 10)


def test_timeintervaltools_TimeInterval_signature_02():
    i = TimeInterval(-30, 3, {'helstart': 'world!'})
    assert i.signature == (-30, 3)
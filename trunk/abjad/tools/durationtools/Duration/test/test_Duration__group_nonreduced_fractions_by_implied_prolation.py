import py
from abjad import *
from abjad.tools.durationtools import Duration
from abjad.tools.mathtools import NonreducedFraction


def test_Duration__group_nonreduced_fractions_by_implied_prolation_01():
    string = 'Duation._group_nonreduced_fractions_by_implied_prolation([])'
    assert py.test.raises(Exception, string)


def test_Duration__group_nonreduced_fractions_by_implied_prolation_02():
    fractions = [(1, 4)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [[NonreducedFraction(1, 4)]]


def test_Duration__group_nonreduced_fractions_by_implied_prolation_03():
    fractions = [(1, 4), (1, 4), (1, 8)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [[
        NonreducedFraction(1, 4), 
        NonreducedFraction(1, 4), 
        NonreducedFraction(1, 8),
        ]]


def test_Duration__group_nonreduced_fractions_by_implied_prolation_04():
    fractions = [(1, 4), (1, 3), (1, 8)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [
        [NonreducedFraction(1, 4)], 
        [NonreducedFraction(1, 3)], 
        [NonreducedFraction(1, 8)],
        ]


def test_Duration__group_nonreduced_fractions_by_implied_prolation_05():
    fractions = [(1, 4), (1, 2), (1, 3)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [
        [NonreducedFraction(1, 4), NonreducedFraction(1, 2)], 
        [NonreducedFraction(1, 3)],
        ]


def test_Duration__group_nonreduced_fractions_by_implied_prolation_06():
    fractions = [(1, 4), (1, 2), (1, 3), (1, 6), (1, 5)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [
        [NonreducedFraction(1, 4), NonreducedFraction(1, 2)], 
        [NonreducedFraction(1, 3), NonreducedFraction(1, 6)], 
        [NonreducedFraction(1, 5)],
        ]


def test_Duration__group_nonreduced_fractions_by_implied_prolation_07():
    fractions = [(1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24)]
    t = Duration._group_nonreduced_fractions_by_implied_prolation(fractions)
    assert t == [[
        NonreducedFraction(1, 24), 
        NonreducedFraction(2, 24), 
        NonreducedFraction(3, 24), 
        NonreducedFraction(4, 24), 
        NonreducedFraction(5, 24), 
        NonreducedFraction(6, 24),
        ]]
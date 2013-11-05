# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_timesignaturetools_establish_metrical_hierarchy_01():

    source = parse('abj: | 4/4 8 2. 8 |')
    target = parse('abj: | 4/4 8 8 ~ 2 ~ 8 8 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source)
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert format(source) == format(target)


def test_timesignaturetools_establish_metrical_hierarchy_02():
    r'''Establishes metrical hierarchy when first component's score offset greater than zero.
    '''

    source = parse('abj: | 2/4 4 4 ~ || 4/4 8 2. 8 ~ || 2/4 4 4 |')
    target = parse('abj: | 2/4 4 4 ~ || 4/4 8 8 ~ 2 ~ 8 8 ~ || 2/4 4 4 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source[1])
    timesignaturetools.establish_metrical_hierarchy(source[1][:], metrical_hierarchy)
    assert format(source) == format(target)


def test_timesignaturetools_establish_metrical_hierarchy_03():
    r'''Descends into tuplets.
    '''

    source = parse('abj: | 2/4 2 ~ || 5/4 8 ~ 8 ~ 2/3 { 4 ~ 4 4 ~ } 4 ~ 4 ~ || 2/4 2 |')
    target = parse('abj: | 2/4 2 ~ || 5/4 4 ~ 2/3 { 2 4 ~ } 2 ~ || 2/4 2 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source[1])
    timesignaturetools.establish_metrical_hierarchy(source[1][:], metrical_hierarchy)
    assert format(source) == format(target)


def test_timesignaturetools_establish_metrical_hierarchy_04():

    source = parse("abj: | 4/4 c'8. d'4.. e'4. |")
    target = parse("abj: | 4/4 c'8. d'16 ~ d'4. e'4. |")
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source)
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert format(source) == format(target)


def test_timesignaturetools_establish_metrical_hierarchy_05():

    metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
    for rhythm_number in range(8):
        # without boundary enforcement
        notes = timesignaturetools.make_gridded_test_rhythm(4, rhythm_number, denominator=4)
        measure = Measure((4, 4), notes)
        timesignaturetools.establish_metrical_hierarchy(measure[:], metrical_hierarchy)
        # with boundary enforcement
        notes = timesignaturetools.make_gridded_test_rhythm(4, rhythm_number, denominator=4)
        measure = Measure((4, 4), notes)
        timesignaturetools.establish_metrical_hierarchy(measure[:], metrical_hierarchy, boundary_depth=-1)


def test_timesignaturetools_establish_metrical_hierarchy_06():

    source = parse('abj: | 4/4 8 4. 2 |')
    target = parse('abj: | 4/4 8 4. 2 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert format(source) == format(target)


def test_timesignaturetools_establish_metrical_hierarchy_07():
    r'''Can limit dot count.
    '''

    metrical_hierarchy = '(4/4 (1/4 1/4 1/4 1/4))'

    maximum_dot_count = None
    source = parse('abj: | 4/4 2... 16 |')
    target = parse('abj: | 4/4 2... 16 |')
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy,
        maximum_dot_count=maximum_dot_count)
    assert format(source) == format(target)

    maximum_dot_count = 3
    source = parse('abj: | 4/4 2... 16 |')
    target = parse('abj: | 4/4 2... 16 |')
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy,
        maximum_dot_count=maximum_dot_count)
    assert format(source) == format(target)

    maximum_dot_count = 2
    source = parse('abj: | 4/4 2... 16 |')
    target = parse('abj: | 4/4 2. ~ 8. 16 |')
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy,
        maximum_dot_count=maximum_dot_count)
    assert format(source) == format(target)

    maximum_dot_count = 1
    source = parse('abj: | 4/4 2... 16 |')
    target = parse('abj: | 4/4 2. ~ 8. 16 |')
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy,
        maximum_dot_count=maximum_dot_count)
    assert format(source) == format(target)

    maximum_dot_count = 0
    source = parse('abj: | 4/4 2... 16 |')
    target = parse('abj: | 4/4 2 ~ 4 ~ 8 ~ 16 16 |')
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy,
        maximum_dot_count=maximum_dot_count)
    assert format(source) == format(target)
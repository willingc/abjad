# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Performer_name_01():

    performer = scoretools.Performer('Flutist')
    assert performer.name == 'Flutist'

    performer.name = 'Violinist'
    assert performer.name == 'Violinist'
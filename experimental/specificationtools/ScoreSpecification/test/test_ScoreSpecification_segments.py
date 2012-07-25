from abjad.tools import *
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_ScoreSpecification_segments_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    assert not specification.segment_specifications


def test_ScoreSpecification_segments_02():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))

    specification.append_segment()
    assert len(specification.segment_specifications) == 1

    specification.append_segment()
    assert len(specification.segment_specifications) == 2

    specification.segment_specifications.pop()
    assert len(specification.segment_specifications) == 1

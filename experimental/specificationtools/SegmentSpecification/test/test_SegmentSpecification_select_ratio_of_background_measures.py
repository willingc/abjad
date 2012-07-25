from abjad.tools import *
from experimental import selectortools
from experimental import specificationtools
from experimental.specificationtools import helpers
from experimental.specificationtools import library


def test_SegmentSpecification_select_ratio_of_background_measures_01():
    
    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)

    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    selector = segment.select_ratio_of_background_measures((1, 1), 0)
    segment.set_divisions(selector, [(3, 16)], truncate=True)

    selector = segment.select_ratio_of_background_measures((1, 1), 1)
    segment.set_divisions(selector, [(5, 16)], truncate=True)

    segment.set_rhythm(segment, library.thirty_seconds)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpers.write_test_output(score, __file__, current_function_name)

    assert score.lilypond_format == helpers.read_test_output(__file__, current_function_name)

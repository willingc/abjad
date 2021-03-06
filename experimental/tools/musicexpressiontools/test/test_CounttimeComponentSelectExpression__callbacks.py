# -*- encoding: utf-8 -*-
from experimental import *


def test_CounttimeComponentSelectExpression__callbacks_01():
    r'''Slice leaves.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves[5:9]
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_02():
    r'''Partition rhythm by ratio.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    left_red_leaves, right_red_leaves = red_leaves.partition_by_ratio((1, 3))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(left_red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_03():
    r'''Partition rhythm by ratio of durations.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    left_red_leaves, right_red_leaves = red_leaves.partition_by_ratio_of_durations((1, 1))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(left_red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_04():
    r'''Repeat to duration.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_duration(Duration(7, 16))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_05():
    r'''Repeat to length.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.repeat_to_length(5)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_06():
    r'''Reflect rhythm.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.reflect()
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_07():
    r'''Rotate rhythm by count.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.rotate(-1)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_08():
    r'''Rotate rhythm by duration.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves.rotate(-Duration(1, 32))
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)


def test_CounttimeComponentSelectExpression__callbacks_09():
    r'''Logical AND of rhythm and timespan.
    '''

    score_template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_rhythm("{ c'16 [ c'8 c'8. ] }")
    red_leaves = red_segment.select_leaves('Voice 1')
    timespan = timespantools.Timespan(Offset(1, 32), Offset(18, 32))
    red_leaves = red_leaves & timespan
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(score, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)

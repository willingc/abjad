# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_AttributeInspectionAgent_get_marks_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())
    command_1 = marktools.LilyPondCommandMark('slurDotted')
    command_1.attach(staff[0])
    command_2 = marktools.LilyPondCommandMark('slurUp')
    command_2.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    marks = inspect(staff[0]).get_marks(marktools.LilyPondCommandMark)
    assert command_1 in marks
    assert command_2 in marks
    assert len(marks) == 2


def test_mutationtools_AttributeInspectionAgent_get_marks_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner()
    slur.attach(staff.select_leaves())
    comment = marktools.LilyPondComment('beginning of note content')
    comment.attach(staff[0])
    command = marktools.LilyPondCommandMark('slurDotted')
    command.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    marks = inspect(staff[0]).get_marks()
    assert comment in marks
    assert command in marks
    assert len(marks) == 2


def test_mutationtools_AttributeInspectionAgent_get_marks_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = contexttools.ClefMark('treble')
    clef.attach(staff)
    dynamic = contexttools.DynamicMark('p')
    dynamic.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        )

    context_marks = inspect(staff[0]).get_marks(contexttools.ContextMark)
    assert dynamic in context_marks
    assert len(context_marks) == 1


def test_mutationtools_AttributeInspectionAgent_get_marks_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = contexttools.ClefMark('treble')
    clef.attach(staff)
    dynamic = contexttools.DynamicMark('p')
    dynamic.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        )

    dynamics = inspect(staff[0]).get_marks(contexttools.DynamicMark)
    assert dynamic in dynamics
    assert len(dynamics) == 1


def test_mutationtools_AttributeInspectionAgent_get_marks_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation_1 = marktools.Annotation('annotation 1')
    annotation_1.attach(staff[0])
    annotation_2 = marktools.Annotation('annotation 2')
    annotation_2.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    annotations = inspect(staff[0]).get_marks(marktools.Annotation)
    assert annotations == (annotation_1, annotation_2)


def test_mutationtools_AttributeInspectionAgent_get_marks_06():

    staff = Staff("c'8 d'8 e'8 f'8")
    comment_1 = marktools.LilyPondComment('comment 1')
    comment_1.attach(staff[0])
    comment_2 = marktools.LilyPondComment('comment 2')
    comment_2.attach(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            % comment 1
            % comment 2
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    marks = inspect(staff[0]).get_marks(marktools.LilyPondComment)
    assert comment_1 in marks
    assert comment_2 in marks
    assert len(marks) == 2


def test_mutationtools_AttributeInspectionAgent_get_marks_07():

    note = Note("c'4")
    stem_tremolo = marktools.StemTremolo(16)
    stem_tremolo.attach(note)
    stem_tremolos = inspect(note).get_marks(marktools.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo
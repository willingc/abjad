# -*- encoding: utf-8 -*-
from abjad import *


def test_formattools_LilyPondFormatManager_report_component_format_contributions_01():
    r'''You can report_component_format_contributions on a heavily 
    tweaked leaf.
    '''

    t = Note("c'4")
    override(t).note_head.style = 'cross'
    override(t).note_head.color = 'red'
    override(t).stem.color = 'red'
    articulation = marktools.Articulation('staccato')
    attach(articulation, t)
    articulation = marktools.Articulation('tenuto')
    attach(articulation, t)
    markup = markuptools.Markup('some markup', Down)
    attach(markup, t)
    comment = marktools.LilyPondComment('textual information before', 'before')
    attach(comment, t)
    comment = marktools.LilyPondComment('textual information after', 'after')
    attach(comment, t)

    assert testtools.compare(
        formattools.LilyPondFormatManager.report_component_format_contributions(t),
        r'''
        slot 1:
            comments:
                % textual information before
            grob overrides:
                \once \override NoteHead #'color = #red
                \once \override NoteHead #'style = #'cross
                \once \override Stem #'color = #red
        slot 3:
        slot 4:
            leaf body:
                c'4 -\staccato -\tenuto _ \markup { some markup }
        slot 5:
        slot 7:
            comments:
                % textual information after
        ''',
        )
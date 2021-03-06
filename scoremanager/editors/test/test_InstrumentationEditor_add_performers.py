# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_add_performers_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation add q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10,)

    input_ = 'red~example~score setup instrumentation add b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (6, 10))

    input_ = 'red~example~score setup instrumentation add h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (0, 10))

    input_ = 'red~example~score setup instrumentation add s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (2, 10))

    input_ = 'red~example~score setup instrumentation add foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (8, 10))


def test_InstrumentationEditor_add_performers_02():
    r'''Add three performers.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentationEditor(session=session)
    input_ = 'add accordionist default add bassoonist default'
    input_ += ' add cellist default q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='accordionist', 
            instruments=[instrumenttools.Accordion()],
            ),
        instrumenttools.Performer(
            name='bassoonist', 
            instruments=[instrumenttools.Bassoon()],
            ),
        instrumenttools.Performer(
            name='cellist', 
            instruments=[instrumenttools.Cello()],
            )])


def test_InstrumentationEditor_add_performers_03():
    r'''Range handling.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentationEditor(session=session)
    input_ = 'add 1-3 default default default q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='accordionist', 
            instruments=[instrumenttools.Accordion()]),
        instrumenttools.Performer(
            name='alto', 
            instruments=[instrumenttools.AltoVoice()]),
        instrumenttools.Performer(
            name='baritone', 
            instruments=[instrumenttools.BaritoneVoice()]),
            ])
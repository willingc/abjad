# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor__run_01():
    r'''Quit, back, home and junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10,)

    input_ = 'red~example~score setup instrumentation hornist b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (6, 10))

    input_ = 'red~example~score setup instrumentation hornist h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (0, 10))

    input_ = 'red~example~score setup instrumentation hornist foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12, (8, 10))

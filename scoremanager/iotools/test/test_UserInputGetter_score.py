# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_score_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation mv s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11, (2, 9))
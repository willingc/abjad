# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_pytest_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory pyt default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.titles[-3] == 'Running py.test ...'
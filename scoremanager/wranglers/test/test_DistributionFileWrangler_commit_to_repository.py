# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_DistributionFileWrangler_commit_to_repository_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score d rci q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_commit_to_repository


def test_DistributionFileWrangler_commit_to_repository_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'd rci q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_commit_to_repository
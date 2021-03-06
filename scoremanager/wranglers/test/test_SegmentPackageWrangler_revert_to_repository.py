# -*- encoding: utf-8 -*-
import pytest
import scoremanager


def test_SegmentPackageWrangler_revert_to_repository_01():
    r'''Flow control reaches method in score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score g rrv default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_revert_to_repository


def test_SegmentPackageWrangler_revert_to_repository_02():
    r'''Flow control reaches method in library.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'g rrv default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_revert_to_repository
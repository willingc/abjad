# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_update_from_repository_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score m rup default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_update_from_repository


def test_MaterialPackageWrangler_update_from_repository_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'm rup default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_update_from_repository
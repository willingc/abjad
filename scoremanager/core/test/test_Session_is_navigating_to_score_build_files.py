# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_build_files_01():
    r'''From build directory to build directory.
    '''

    input_ = 'red~example~score u u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_02():
    r'''From distribution directory to build directory.
    '''

    input_ = 'red~example~score d u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_03():
    r'''From makers directory to build directory.
    '''

    input_ = 'red~example~score k u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_04():
    r'''From materials directory to build directory.
    '''

    input_ = 'red~example~score m u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_05():
    r'''From segments directory to build directory.
    '''

    input_ = 'red~example~score g u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_06():
    r'''From setup menu to build directory.
    '''

    input_ = 'red~example~score p u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_build_files_07():
    r'''From stylesheets directory to build directory.
    '''

    input_ = 'red~example~score y u q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - build directory',
        ]
    assert score_manager._transcript.titles == titles
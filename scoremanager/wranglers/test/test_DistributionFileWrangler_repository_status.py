# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_repository_status_01():
    r'''Works with distribution file library.
    '''
    pytest.skip('add some distribution files to red example score.')

    input_ = 'd rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_DistributionFileWrangler_repository_status_02():
    r'''Works with Git-managed score.
    '''

    input_ = 'red~example~score d rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_DistributionFileWrangler_repository_status_03():
    r'''Works with Subversion-managed score.
    '''

    score_name = score_manager._find_svn_score_name()
    if not score_name:
        return

    input_ = 'ssl {} d rst default q'.format(score_name)
    score_manager._run(pending_user_input=input_)

    string = 'Press return to continue.'
    assert string in score_manager._transcript.titles
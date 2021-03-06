# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_repository_status_01():
    r'''Works with library.
    '''

    input_ = 'k rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_MakerModuleWrangler_repository_status_02():
    r'''Works with Git-managed makers directory.
    '''

    input_ = 'red~example~score k rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_MakerModuleWrangler_repository_status_03():
    r'''Works with Subversion-managed makers directory.
    '''

    score_name = score_manager._find_svn_score_name()
    if not score_name:
        return

    input_ = 'ssl {} k rst default q'.format(score_name)
    score_manager._run(pending_user_input=input_)

    string = 'Press return to continue.'
    assert string in score_manager._transcript.titles
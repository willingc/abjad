# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q')
    assert score_manager._session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='lmm b q')
    assert score_manager._session.io_transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input='lmm h q')
    assert score_manager._session.io_transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input='lmm s q')
    assert score_manager._session.io_transcript.signature == (6, (2, 4))

    score_manager._run(pending_user_input='lmm asdf q')
    assert score_manager._session.io_transcript.signature == (6, (2, 4))


def test_MaterialPackageWrangler__run_02():
    r'''Breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q')
    title_line = 'Score manager - material library'
    assert score_manager._session.io_transcript.last_menu_title == title_line


def test_MaterialPackageWrangler__run_03():
    r'''Menu displays at least one test material.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q')
    menu_lines = score_manager._session.io_transcript.last_menu_lines
    assert any(x.endswith('red sargasso measures') for x in menu_lines)
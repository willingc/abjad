# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager_copy_01():

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary-file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new-temporary-file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    file_manager = scoremanager.managers.FileManager(
        path=path,
        session=session,
        )

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        input_ = 'new-temporary-file.txt y q'
        file_manager._session._pending_user_input = input_
        file_manager.copy()
        assert os.path.exists(path)
        assert os.path.exists(new_path)
        file_manager._remove()
        os.remove(new_path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
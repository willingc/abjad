# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager


def test_ListMaterialManager_edit_output_material_01():
    pytest.skip('make autoadding work again.')

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testlist',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output.py',
        ]
    input_ = 'm nmm list testlist 17 foo done b default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ListMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == [17, 'foo']
        input_ = 'm testlist rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialPackageWrangler_make_handmade_material_package_01():
    r'''Package is created and directory contents are correct.
    '''

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'definition.py', 
        ]

    assert not os.path.exists(path)
    try:
        input_ = 'testnotes q'
        wrangler._session._pending_user_input = input_
        wrangler.make_handmade_material_package()
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_handmade_material_package_02():
    r'''Empty material definition module is correct.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    definition_module_path = os.path.join(
        path,
        'definition.py',
        )

    lines = []
    lines.append('# -*- encoding: utf-8 -*-')
    lines.append('from abjad import *')
    lines.append('output_module_import_statements = []')
    lines.append('')
    lines.append('')
    lines.append('testnotes = None')
    contents = '\n'.join(lines)

    assert not os.path.exists(path)
    try:
        input_ = 'm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        with file(definition_module_path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
        file_contents = ''.join(file_lines)
        assert file_contents == contents
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
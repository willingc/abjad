# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryMaterialManager_edit_output_material_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testoctavetrans',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]
    input_ = 'm nmm octave testoctavetrans default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.OctaveTranspositionMappingInventoryMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'm testoctavetrans rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_OctaveTranspositionMappingInventoryMaterialManager_edit_output_material_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testoctavetrans',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output.py',
        ]
    mapping_1 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C4)', 15), 
        ('[C4, C8)', 27),
        ])
    mapping_2 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C8]', -18),
        ])
    inventory = pitchtools.OctaveTranspositionMappingInventory([
        mapping_1, 
        mapping_2
        ])
    input_ = 'm nmm octave testoctavetrans'
    input_ += ' testoctavetrans me add add source [A0, C4) target 15 done'
    input_ += ' add source [C4, C8) target 27 done done'
    input_ += ' add add source [A0, C8] target -18 done done done default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.OctaveTranspositionMappingInventoryMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == inventory
        input_ = 'm testoctavetrans rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)

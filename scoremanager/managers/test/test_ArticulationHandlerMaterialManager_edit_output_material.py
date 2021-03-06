# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
from experimental import *
import scoremanager


def test_ArticulationHandlerMaterialManager_edit_output_material_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testarticulationhandler',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output.py', 
        ]
    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )
    input_ = 'm nmm articulation testarticulationhandler default'
    input_ += ' reiterated'
    input_ += " ['^', '.'] (1, 64) (1, 4) c c'''' done default"
    input_ += ' q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ArticulationHandlerMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == handler
        input_ = 'm testarticulationhandler rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)

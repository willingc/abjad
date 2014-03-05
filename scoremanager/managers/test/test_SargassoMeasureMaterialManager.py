# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_SargassoMeasureMaterialManager_01():
    r'''Empty wrapper.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_02():
    r'''Load demo values.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)

    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uil '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', True),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_03():
    r'''Load demo values and then clear all.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uil uic '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', None),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_04():
    r'''Edit one value.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso 3 16 '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', None),
            ('measure_numerator_talea', None),
            ('measure_division_denominator', 16),
            ('measure_division_talea', None),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_05():
    r'''Populate wrapper.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uip 5 '
            'Duration(11, 2) False True True 4 [2, 2, 2, 2, 1, 1, 4, 4] 16 [1, 1, 2, 3, 4] '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', False),
            ('measures_are_split', True),
            ('measures_are_shuffled', True)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_06():
    r'''Partial population.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uip 1 '
            '4 [2, 2, 3, 3] 16 [1, 1, 1, 1, 6, 6] b '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 3, 3]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 1, 1, 6, 6]),
            ('total_duration', None),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_07():
    r'''Set some values to none.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uil 6 None 7 None 8 None '
            'q'
            )
        #string = 'scoremanager.materials.testsargasso'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('measure_denominator', 4),
            ('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
            ('measure_division_denominator', 16),
            ('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
            ('total_duration', Duration(11, 2)),
            ('measures_are_scaled', None),
            ('measures_are_split', None),
            ('measures_are_shuffled', None)])
        assert manager._user_input_wrapper_in_memory == user_input_wrapper
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)


def test_SargassoMeasureMaterialManager_08():
    r'''Make output from demo values.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        'user_input.py',
        ]
    measures = [
        scoretools.Measure((4, 16), "c'16 c'16 c'8"),
        scoretools.Measure((2, 10), "c'8 c'8"),
        scoretools.Measure((3, 20), "c'8 c'16"),
        scoretools.Measure((4, 16), "c'8. c'16"),
        scoretools.Measure((4, 16), "c'8. c'16"),
        scoretools.Measure((11, 30), "c'16 c'16 c'8 c'8. c'4"),
        scoretools.Measure((15, 30), "c'8 c'16 c'8 c'8. c'4 c'16 c'16 c'16"),
        scoretools.Measure((2, 8), "c'8 c'8"),
        scoretools.Measure((10, 26), "c'8 c'8. c'4 c'16"),
        scoretools.Measure((4, 30), "c'16 c'16 c'16 c'16"),
        scoretools.Measure((15, 30), "c'16 c'4 c'16 c'16 c'8 c'8. c'16 c'8"),
        scoretools.Measure((7, 26), "c'16 c'4 c'16 c'16"),
        scoretools.Measure((3, 26), "c'16 c'16 c'16"),
        scoretools.Measure((1, 4), "c'4"),
        scoretools.Measure((10, 19), "c'8. c'4 c'16 c'16 c'16"),
        scoretools.Measure((6, 26), "c'16 c'16 c'4"),
        scoretools.Measure((6, 20), "c'4 c'16 c'16"),
        scoretools.Measure((2, 20), "c'16 c'16"),
        scoretools.Measure((9, 19), "c'16 c'4 c'16 c'16 c'8")]
    for measure in measures:
        measure.implicit_scaling = True

    try:
        score_manager._run(pending_user_input=
            'lmm nmm sargasso testsargasso default '
            'testsargasso uil omm default '
            'q'
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testsargasso')
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        assert format(Staff(measures))
        output_material = manager._execute_output_material_module()
        for measure in output_material:
            assert measure.implicit_scaling
        assert format(Staff(output_material))
        assert format(Staff(output_material)) == format(Staff(measures))
    finally:
        string = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testsargasso'
        assert not score_manager._configuration.package_exists(string)
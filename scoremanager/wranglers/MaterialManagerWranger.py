# -*- encoding: utf-8 -*-
import os
from abjad.tools import layouttools
from abjad.tools import lilypondfiletools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MaterialManagerWrangler(Wrangler):
    r'''material manager wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> wrangler = score_manager._material_manager_wrangler
            >>> wrangler
            MaterialManagerWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_human_readable_target_name',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MaterialManagerWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = \
            self._configuration.abjad_material_managers_directory_path
        self._user_storehouse_path = \
            self._configuration.user_library_material_managers_directory_path
        self._human_readable_target_name = 'material manager'
        self._forbidden_directory_entries = (
            'InventoryMaterialManager.py',
            'MaterialManager.py',
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.MaterialManagerWrangler

    @property
    def _breadcrumb(self):
        return 'material managers'

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialManagerWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _get_current_directory_path_of_interest(self):
        pass

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            raise ValueError

    def _initialize_asset_manager(self, path):
        from scoremanager import managers
        assert os.path.sep in path, repr(path)
        material_manager = managers.MaterialManager(
            path=path, 
            session=self._session,
            )
        if 'managers' in material_manager._path:
            most, last = os.path.split(material_manager._path)
            material_manager_class_name = os.path.splitext(last)[0]
        else:
            material_manager_class_name = \
                material_manager._read_material_manager_class_name()
        if material_manager_class_name is not None:
            material_manager_class = None
            command = 'from scoremanager'
            command += '.managers '
            command += 'import {} as material_manager_class'
            command = command.format(material_manager_class_name)
            try:
                exec(command)
            except ImportError:
                command = 'from {} import {} as material_manager_class'
                path = self._configuration.user_library_material_packages_directory_path
                package_path = self._configuration.path_to_package_path(path)
                command = command.format(
                    package_path,
                    material_manager_class_name,
                    )
                exec(command)
            material_manager = material_manager_class(
                path=path, 
                session=self._session,
                )
        return material_manager

    def _is_valid_directory_entry(self, directory_entry):
        if directory_entry in ('test', 'stylesheets'):
            return False
        if directory_entry.endswith('.pyc'):
            return False
        if directory_entry in self._forbidden_directory_entries:
            return False
        if not directory_entry.endswith('MaterialManager.py'):
            return False
        if directory_entry[0].isalpha():
            if directory_entry[0].isupper():
                return True
        return False

    def _make_main_menu(self, name='material manager wrangler'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        asset_section = menu.make_asset_section()
        asset_menu_entries = self._make_asset_menu_entries()
        for menu_entry in asset_menu_entries:
            asset_section.append(menu_entry)
        section = menu.make_command_section()
        section.append(('material manager - new', 'new'))
        return menu
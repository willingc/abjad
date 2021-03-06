# -*- encoding: utf-8 -*-
import os
import subprocess
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class ScoreManager(Controller):
    r'''Score manager.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> score_manager
            ScoreManager()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, is_test=False):
        from scoremanager import core
        if session is None:
            session = core.Session()
            session._is_test = is_test
        Controller.__init__(self, session=session)
        self._session._score_manager = self

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.current_controller is self:
            result = 'score manager - {}'
            result = result.format(self._score_status_string)
            return result
        elif self._session.is_in_score:
            return
        else:
            return 'score manager'

    @property
    @systemtools.Memoize
    def _build_file_wrangler(self):
        from scoremanager import wranglers
        return wranglers.BuildFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _distribution_file_wrangler(self):
        from scoremanager import wranglers
        return wranglers.DistributionFileWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _maker_module_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MakerModuleWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _material_manager_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MaterialManagerWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _material_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.MaterialPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _score_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.ScorePackageWrangler(session=self._session)

    @property
    def _score_status_string(self):
        return '{} scores'.format(self._session.scores_to_display)

    @property
    @systemtools.Memoize
    def _segment_package_wrangler(self):
        from scoremanager import wranglers
        return wranglers.SegmentPackageWrangler(session=self._session)

    @property
    @systemtools.Memoize
    def _stylesheet_wrangler(self):
        from scoremanager import wranglers
        return wranglers.StylesheetWrangler(session=self._session)

    @property
    def _user_input_to_action(self):
        result = {
            'cro': self.view_cache,
            'cw': self.write_cache,
            'd': self.manage_distribution_artifact_library,
            'fix': self.fix_score_packages,
            'g': self.manage_segment_library,
            'k': self.manage_maker_library,
            'm': self.manage_material_library,
            'mdme': self.edit_metadata_modules,
            'mdmls': self.list_metadata_modules,
            'mdmrw': self.rewrite_metadata_modules,
            'new': self.make_new_score,
            'pyd': self.doctest,
            'pyt': self.pytest,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'rrv': self.revert_to_repository,
            'rst': self.repository_status,
            'rup': self.update_from_repository,
            'ssl': self.display_all_scores,
            'ssv': self.display_active_scores,
            'ssmb': self.display_mothballed_scores,
            'ssx': self.display_example_scores,
            'ssu': self.display_user_scores,
            'u': self.manage_build_file_library,
            'y': self.manage_stylesheet_library,
            }
        return result

    ### PRIVATE METHODS ###

    def _find_svn_score_name(self):
        from scoremanager import managers
        manager = self._find_up_to_date_manager(
            managers.ScorePackageManager,
            repository='svn',
            system=False,
            )
        if manager:
            title = manager._get_title()
            title = stringtools.string_to_accent_free_snake_case(title)
            return title

    def _find_up_to_date_manager(
        self, 
        manager_class,
        repository='git',
        system=True,
        ):
        import scoremanager
        session = scoremanager.core.Session()
        manager = manager_class(session=session)
        suffix = getattr(manager, '_score_directory_suffix', None)
        suffix = suffix or ()
        if isinstance(suffix, str):
            suffix = (suffix,)
        assert isinstance(suffix, tuple)
        if system:
            scores_directory = \
                self._configuration.abjad_score_packages_directory_path
        else:
            scores_directory = \
                self._configuration.user_score_packages_directory_path
        for score_package_name in os.listdir(scores_directory):
            path = os.path.join(
                scores_directory, 
                score_package_name, 
                *suffix
                )
            if not os.path.isdir(path):
                continue
            session = scoremanager.core.Session(is_test=True)
            manager = manager_class(path=path, session=session)
            if repository == 'git' and \
                manager._is_git_versioned() and \
                manager._is_up_to_date():
                return manager
            elif repository == 'svn' and \
                manager._is_svn_versioned() and \
                manager._is_up_to_date():
                return manager

    # TODO: combine paired methods
    def _get_next_score_directory_path(self):
        wrangler = self._score_package_wrangler
        paths = wrangler._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            return paths[0]
        score_path = self._session.last_asset_path
        index = paths.index(score_path)
        next_index = (index + 1) % len(paths)
        next_path = paths[next_index]
        return next_path

    # TODO: combine paired methods
    def _get_previous_score_directory_path(self):
        wrangler = self._score_package_wrangler
        paths = wrangler._list_visible_asset_paths()
        if self._session.last_asset_path is None:
            return paths[-1]
        path = self._session.last_asset_path
        index = paths.index(path)
        previous_index = (index - 1) % len(paths)
        previous_path = paths[previous_index]
        return previous_path

    def _get_scores_to_display_string(self):
        return '{} scores'.format(self._session.scores_to_display)

    def _get_sibling_score_path(self):
        if self._session.is_navigating_to_next_score:
            self._session._is_navigating_to_next_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_next_score_directory_path()
        if self._session.is_navigating_to_previous_score:
            self._session._is_navigating_to_previous_score = False
            self._session._is_backtracking_to_score_manager = False
            return self._get_previous_score_directory_path()

    def _get_wrangler_navigation_directive(self):
        if self._session.is_navigating_to_score_build_files:
            return 'u'
        elif self._session.is_navigating_to_score_distribution_files:
            return 'd'
        elif self._session.is_navigating_to_score_maker_modules:
            return 'k'
        elif self._session.is_navigating_to_score_materials:
            return 'm'
        elif self._session.is_navigating_to_score_segments:
            return 'g'
        elif self._session.is_navigating_to_score_stylesheets:
            return 'y'

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            wrangler = self._score_package_wrangler
            score_package_paths = wrangler._list_visible_asset_paths()
            if result in score_package_paths:
                self.manage_score(result)

    def _list_all_directories_with_metadata_modules(self):
        storehouses = (
            self._configuration.abjad_material_packages_directory_path,
            self._configuration.abjad_score_packages_directory_path,
            self._configuration.user_library_directory_path,
            self._configuration.user_score_packages_directory_path,
            )
        directories = []
        for storehouse in storehouses:
            result = self._list_directories_with_metadata_modules(storehouse)
            directories.extend(result)
        return directories

    def _make_all_directories_menu_section(self, menu):
        section = menu.make_command_section(
            name='all dirs',
            is_hidden=True,
            )
        string = 'all dirs - metadata module - edit'
        section.append((string, 'mdme'))
        string = 'all dirs - metadata module - list'
        section.append((string, 'mdmls'))
        string = 'all dirs - metadata module - rewrite'
        section.append((string, 'mdmrw'))
        return section

    def _make_all_score_packages_menu_section(self, menu):
        section = menu.make_command_section(
            name='all score packages',
            is_hidden=True,
            )
        string = 'all score packages - fix'
        section.append((string, 'fix'))
        return section

    def _make_cache_menu_section(self, menu):
        section = menu.make_command_section(
            name='cache',
            is_hidden=True,
            )
        section.append(('cache - read only', 'cro'))
        section.append(('cache - write', 'cw'))
        return menu

    def _make_library_menu_section(self, menu):
        section = menu.make_command_section(
            name='library',
            is_hidden=True,
            )
        section.append(('library - build files', 'u'))
        section.append(('library - distribution files', 'd'))
        section.append(('library - makers', 'k'))
        section.append(('library - materials', 'm'))
        section.append(('library - segments', 'g'))
        section.append(('library - stylesheets', 'y'))
        return section

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        self._make_all_directories_menu_section(menu)
        self._make_all_score_packages_menu_section(menu)
        self._make_library_menu_section(menu)
        self._make_scores_menu_section(menu)
        self._make_scores_show_menu_section(menu)
        self._make_cache_menu_section(menu)
        return menu

    def _make_score_selection_menu(self):
        wrangler = self._score_package_wrangler
        if self._session.rewrite_cache:
            self._io_manager.write_cache(prompt=False)
            self._session._rewrite_cache = False
        menu_entries = self._io_manager._read_cache()
        if not menu_entries or \
            (self._session._scores_to_display == 'example' and
            not menu_entries[0][0] == 'Blue Example Score (2013)'):
            self._io_manager.write_cache(prompt=False)
            menu_entries = self._io_manager._read_cache()
        menu = self._io_manager.make_menu(
            where=self._where,
            name='main',
            breadcrumb_callback=self._get_scores_to_display_string,
            )
        section = menu.make_asset_section()
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return menu

    def _make_scores_menu_section(self, menu):
        section = menu.make_command_section(
            name='scores - new',
            )
        section.append(('scores - new', 'new'))
        return section

    def _make_scores_show_menu_section(self, menu):
        section = menu.make_command_section(
            name='scores - show',
            is_hidden=True,
            )
        section.append(('scores - show all', 'ssl'))
        section.append(('scores - show active', 'ssv'))
        section.append(('scores - show examples', 'ssx'))
        section.append(('scores - show mothballed', 'ssmb'))
        section.append(('scores - show user', 'ssu'))
        return section

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        self._session._reinitialize()
        type(self).__init__(self, session=self._session)
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context =  iotools.ControllerContext(
            self,
            on_exit_callbacks=(self._session._clean_up,)
            )
        with context:
            while True:
                result = self._get_sibling_score_path()
                if not result:
                    result = self._get_wrangler_navigation_directive()
                if not result:
                    menu = self._make_main_menu()
                    result = menu._run()
                if self._should_backtrack():
                    return
                if result:
                    self._handle_main_menu_result(result)
                    if self._should_backtrack():
                        return

    def _should_backtrack(self):
        self._update_session_variables()
        if self._session.is_complete:
            return True
        else:
            return False

    def _update_session_variables(self):
        if self._session.is_backtracking_to_score_manager:
            self._session._is_backtracking_to_score_manager = False
        if self._session.is_backtracking_to_score:
            self._session._is_backtracking_to_score = False

    ### PUBLIC METHODS ###

    def add_to_repository(self, prompt=True):
        r'''Adds assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.add_to_repository(prompt=prompt)

    def commit_to_repository(self, prompt=True):
        r'''Commits assets to repository.

        Returns none.
        '''
        self._score_package_wrangler.commit_to_repository()

    def display_active_scores(self):
        r'''Displays active scores.

        Returns none.
        '''
        self._session.display_active_scores()

    def display_all_scores(self):
        r'''Displays all scores.

        Returns none.
        '''
        self._session.display_all_scores()

    def display_example_scores(self):
        r'''Displays example scores.

        Returns none.
        '''
        self._session.display_example_scores()

    def display_mothballed_scores(self):
        r'''Displays mothballed scores.

        Returns none.
        '''
        self._session.display_mothballed_scores()

    def display_user_scores(self):
        r'''Displays user scores.

        Returns none.
        '''
        self._session.display_user_scores()

    def doctest(self, prompt=True):
        r'''Runs doctest.

        Returns none.
        '''
        if self._session.is_test:
            return
        path = self._configuration.user_score_packages_directory_path
        command = 'ajv doctest {}'.format(path)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def edit_metadata_modules(self):
        r'''Edits all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        from scoremanager import managers
        directories = self._list_all_directories_with_metadata_modules()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        self._io_manager.view(paths)

    def fix_score_packages(self, prompt=True):
        r'''Fixes score packages.

        Returns none.
        '''
        from scoremanager import managers
        wrangler = self._score_package_wrangler
        paths = wrangler._list_visible_asset_paths()
        for path in paths:
            manager = managers.ScorePackageManager(
                path=path,
                session=self._session,
                )
            needed_to_be_fixed = manager.fix(prompt=prompt)
            if not needed_to_be_fixed:
                title = manager._get_title()
                message = '{} OK.'
                message = message.format(title)
                self._io_manager.display(message)
        message = '{} score packages checked.'
        message = message.format(len(paths))
        self._io_manager.display(['', message, ''])
        self._io_manager.proceed(prompt=prompt)

    def list_metadata_modules(self, prompt=True):
        r'''Lists all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        from scoremanager import managers
        directories = self._list_all_directories_with_metadata_modules()
        paths = [os.path.join(_, '__metadata__.py') for _ in directories]
        lines = paths[:]
        lines.append('')
        if prompt:
            self._io_manager.display(lines)
        message = '{} metadata modules found.'
        message = message.format(len(paths))
        self._io_manager.proceed(message, prompt=prompt)

    def make_new_score(self):
        r'''Makes new score.

        Returns none.
        '''
        self._score_package_wrangler.make_new_score()

    def manage_build_file_library(self):
        r'''Manages build file library.

        Returns none.
        '''
        self._build_file_wrangler._run()

    def manage_distribution_artifact_library(self):
        r'''Manages distribution file library.

        Returns none.
        '''
        self._distribution_file_wrangler._run()

    def manage_maker_library(self):
        r'''Manages maker library.

        Returns none.
        '''
        self._maker_module_wrangler._run()

    def manage_material_library(self):
        r'''Manages material library.

        Returns none.
        '''
        self._material_package_wrangler._run()

    def manage_score(self, path):
        r'''Manages score.

        Returns none.
        '''
        manager = self._score_package_wrangler._initialize_asset_manager(path)
        package_name = os.path.basename(path)
        manager.fix(prompt=True)
        manager._run()

    def manage_segment_library(self):
        r'''Manages segment library.

        Returns none.
        '''
        self._segment_package_wrangler._run()

    def manage_stylesheet_library(self):
        r'''Manages stylesheet library.

        Returns none.
        '''
        self._stylesheet_wrangler._run()

    def pytest(self, prompt=True):
        r'''Runs py.test.

        Returns none.
        '''
        if self._session.is_test:
            return
        path = self._configuration.user_score_packages_directory_path
        command = 'py.test -rf {}'
        command = command.format(path)
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE,
            )
        lines = [line.strip() for line in process.stdout.readlines()]
        if lines:
            lines.append('')
            self._io_manager.display(
                lines, 
                capitalize_first_character=False,
                )
        self._io_manager.proceed(prompt=prompt)

    def repository_status(self, prompt=True):
        r'''Displays status of repository assets.
        
        Returns none.
        '''
        self._score_package_wrangler.repository_status(prompt=prompt)

    def revert_to_repository(self, prompt=True):
        r'''Reverts modified assets and unadds added assets.

        Returns none.
        '''
        self._score_package_wrangler.revert_to_repository(prompt=prompt)

    def rewrite_metadata_modules(self, prompt=True):
        r'''Rewrites all metadata modules everywhere.

        Ignores view.

        Returns none.
        '''
        from scoremanager import managers
        directories = self._list_all_directories_with_metadata_modules()
        for directory in directories:
            manager = managers.PackageManager(
                path=directory, 
                session=self._session,
                )
            manager.rewrite_metadata_module(prompt=False)
        message = '{} metadata modules found.'
        message = message.format(len(directories))
        self._io_manager.proceed(message, prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Updates repository assets.

        Returns none.
        '''
        self._score_package_wrangler.update_from_repository()

    def view_cache(self):
        r'''Views cache.

        Returns none.
        '''
        file_path = self._configuration.cache_file_path
        self._io_manager.open_file(file_path)
        self._session._hide_next_redraw = True

    def write_cache(self, prompt=True):
        r'''Writes cache.

        Returns none.
        '''
        self._io_manager.write_cache(prompt=prompt)
import abc
import os
from abjad.tools import stringtools
from experimental.tools import packagepathtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject


class FilesystemAssetWrangler(ScoreManagerObject):
    '''Filesystem asset wrangler.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self,
        system_asset_container_directory_paths=None,
        system_asset_container_package_paths=None,
        user_asset_container_directory_paths=None,
        session=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._system_asset_container_directory_paths = \
            system_asset_container_directory_paths or []
        self._system_asset_container_package_paths = \
            system_asset_container_package_paths or []
        self._user_asset_container_directory_paths = \
            user_asset_container_directory_paths or []

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when system and user asset container paths are both equal.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.system_asset_container_directory_paths == \
                expr.system_asset_container_directory_paths:
                if self.user_asset_container_directory_paths == \
                    expr.user_asset_container_directory_paths:
                        return True
        return False

    def __repr__(self):
        '''Filesystem asset wrangler repr.

        Return string.
        '''
        parts = []
        parts.extend(self.system_asset_container_directory_paths)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self._class_name, parts)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _temporary_asset_name(self):
        pass

    ### PRIVATE METHODS ###

    def _filesystem_path_to_space_delimited_lowercase_name(self, filesystem_path):
        filesystem_path = os.path.normpath(filesystem_path)
        asset_name = os.path.basename(filesystem_path)
        asset_name = self.strip_file_extension_from_file_name(asset_name)
        return stringtools.string_to_space_delimited_lowercase(asset_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def asset_class(self):
        pass

    @property
    def asset_container_class(self):
        from experimental.tools import scoremanagertools
        return scoremanagertools.proxies.DirectoryProxy

    @property
    def current_asset_container_proxy(self):
        return self.asset_container_class(self.current_asset_container_filesystem_path)

    @property
    def system_asset_container_directory_paths(self):
        return self._system_asset_container_directory_paths

    @property
    def system_asset_container_package_paths(self):
        return self._system_asset_container_package_paths

    @property
    def temporary_asset_filesystem_path(self):
        return os.path.join(self.current_asset_container_directory_path, self._temporary_asset_name)

    @property
    def temporary_asset_proxy(self):
        return self.get_asset_proxy(self.temporary_asset_filesystem_path)

    @property
    def user_asset_container_directory_paths(self):
        return self._user_asset_container_directory_paths
    
    ### PUBLIC METHODS ###

    def fix_visible_assets(self, is_interactive=True):
        results = []
        for asset_proxy in self.list_visible_asset_proxies():
            results.append(asset_proxy.fix(is_interactive=is_interactive))
            if is_interactive:
                asset_proxy.profile()
        return results

    def get_asset_proxy(self, asset_filesystem_path):
        return self.asset_class(asset_filesystem_path, session=self.session)

    @abc.abstractmethod
    def handle_main_menu_result(self, result):
        pass

    def list_asset_container_directory_paths(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_directory_paths(head=head))
        result.extend(self.list_score_internal_asset_container_directory_paths(head=head))
        return result

    def list_asset_container_proxies(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_proxies(head=head))
        result.extend(self.list_score_internal_asset_container_proxies(head=head))
        return result

    # assets (all) #

    def list_asset_filesystem_paths(self, head=None):
        result = []
        if head in (None,) + self.configuration.system_package_paths:
            result.extend(self.list_score_external_asset_filesystem_paths(head=head))
        result.extend(self.list_score_internal_asset_filesystem_paths(head=head))
        result.extend(self.list_user_asset_filesystem_paths(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(head=head):
            asset_proxy = self.get_asset_proxy(filesystem_path)
            result.append(asset_proxy)
        return result

    # score-external asset containers #

    # TODO: rewrite purely in terms of directory paths (instead of package paths)
    def list_score_external_asset_container_directory_paths(self, head=None):
        result = []
        for package_path in self.list_system_asset_container_package_paths(head=head):
            result.append(packagepathtools.package_path_to_directory_path(package_path))
        return result

    # TODO: rewrite purley in terms of directory paths (instead of package paths)
    def list_score_external_asset_container_proxies(self, head=None):
        result = []
        for package_path in self.list_system_asset_container_package_paths(head=head):
            asset_container_proxy = self.asset_container_class(package_path)
            result.append(asset_container_proxy)
        return result

    def list_score_external_asset_filesystem_paths(self, head=None):
        result = []
        for directory_path in self.list_score_external_asset_container_directory_paths(head=head):
            for directory_entry in os.listdir(directory_path):
                if directory_entry[0].isalpha():
                    filesystem_path = os.path.join(directory_path, directory_entry)
                    result.append(filesystem_path)
        return result

    def list_score_external_asset_proxies(self, head=None):
        result = []
        for filesystem_path in self.list_score_external_asset_filesystem_paths(head=head):
            asset_proxy = self.get_asset_proxy(filesystem_path)
            result.append(asset_proxy)
        return result

    # score-internal asset containers #

    def list_score_internal_asset_container_directory_paths(self, head=None):
        result = []
        for package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            result.append(packagepathtools.package_path_to_directory_path(package_path))
        return result

    def list_score_internal_asset_container_package_paths(self, head=None):
        result = []
        for score_package_name in self.list_score_package_names(head=head):
            parts = [score_package_name]
            if self.score_internal_asset_container_package_path_infix:
                parts.append(self.score_internal_asset_container_package_path_infix)
            score_internal_score_package_path = '.'.join(parts)
            result.append(score_internal_score_package_path)
        return result

    def list_score_internal_asset_container_proxies(self, head=None):
        result = []
        for package_path in \
            self.list_score_internal_asset_container_package_paths(head=head):
            asset_container_proxy = self.asset_container_class(package_path)
            result.append(asset_container_proxy)
        return result

    # score-internal assets #

    def list_score_internal_asset_filesystem_paths(self, head=None):
        result = []
        for asset_filesystem_path in self.list_score_internal_asset_container_directory_paths(head=head):
            for name in os.listdir(asset_filesystem_path):
                if name[0].isalpha():
                    result.append(os.path.join(asset_filesystem_path, name))
        return result

    def list_score_internal_asset_proxies(self, head=None):
        result = []
        for package_path in self.list_score_internal_asset_package_paths(head=head):
            asset_proxy = self.asset_class_name(package_path)
            result.append(asset_proxy)
        return result

    def list_score_package_names(self, head=None):
        result = []
        for name in os.listdir(self.configuration.user_scores_directory_path):
            if name[0].isalpha():
                if head and name == head:
                    return [name]
                elif not head:
                    result.append(name)
        return result

    def list_space_delimited_lowercase_asset_container_names(self, head=None):
        directory_paths, result = [], []
        directory_paths.extend(self.list_score_external_asset_container_directory_paths(head=head))
        directory_paths.extend(self.list_score_internal_asset_container_directory_paths(head=head))
        for directory_path in directory_paths:
            name = self._filesystem_path_to_space_delimited_lowercase_name(directory_path)
            result.append(name)
        return result

    def list_space_delimited_lowercase_asset_names(self, head=None):
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(head=head):
            result.append(self._filesystem_path_to_space_delimited_lowercase_name(filesystem_path))
        return result

    def list_space_delimited_lowercase_visible_asset_names(self, head=None):
        result = []
        for filesystem_path in self.list_visible_asset_filesystem_paths(head=head):
            result.append(self._filesystem_path_to_space_delimited_lowercase_name(filesystem_path))
        return result

    def list_system_asset_container_package_paths(self, head=None):
        result = []
        for package_path in self._system_asset_container_package_paths:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    # user asset containers #

    def list_user_asset_container_directory_paths(self, head=None):
        return self.user_asset_container_directory_paths[:]

    def list_user_asset_container_package_paths(self, head=None):
        result = []
        for package_path in self._user_asset_container_package_paths:
            if head is None or package_path.startswith(head):
                result.append(package_path)
        return result

    def list_user_asset_container_proxies(self, head=None):
        result = []
        for package_path in self.list_user_asset_container_package_paths(head=head):
            asset_container_proxy = self.asset_container_class(package_path)
            result.append(asset_container_proxy)
        return result

    def list_user_asset_filesystem_paths(self, head=None):
        result = []
        for asset_filesystem_path in self.list_user_asset_container_directory_paths(head=head):
            for name in os.listdir(asset_filesystem_path):
                if name[0].isalpha():
                    result.append(os.path.join(asset_filesystem_path, name))
        return result

    def list_user_asset_proxies(self, head=None):
        result = []
        for asset_filesystem_path in self.list_user_asset_filesystem_paths(head=head):
            asset_proxy = self.get_asset_proxy(asset_filesystem_path)
            result.append(asset_proxy)
        return result

    def list_visible_asset_filesystem_paths(self, head=None):
        return self.list_asset_filesystem_paths(head=head)

    def list_visible_asset_proxies(self, head=None):
        return self.list_asset_proxies(head=head)

    def make_asset(self, asset_name):
        assert stringtools.is_underscore_delimited_lowercase_string(asset_name)
        asset_filesystem_path = os.path.join(self.current_asset_container_directory_path, asset_name)
        asset_proxy = self.get_asset_proxy(asset_filesystem_path)
        asset_proxy.write_stub_to_disk()

    @abc.abstractmethod
    def make_asset_interactively(self):
        pass

    def make_asset_selection_breadcrumb(self, infinitival_phrase=None):
        if infinitival_phrase:
            return 'select {} {}:'.format(self.asset_class._generic_class_name, infinitival_phrase)
        else:
            return 'select {}:'.format(self.asset_class._generic_class_name)

    def make_asset_selection_menu(self, head=None):
        menu, section = self.io.make_menu(where=self.where(), is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        #self.debug(section.tokens, 'TOKENS')
        section.return_value_attribute = 'key'
        return menu

    @abc.abstractmethod
    def make_main_menu(self):
        pass

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_filesystem_paths(head=head)
        bodies = self.list_space_delimited_lowercase_visible_asset_names(head=head)
        return zip(keys, bodies)

    def profile_visible_assets(self):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.profile()

    # TODO: write test
    def remove_assets_interactively(self, head=None):
        getter = self.io.make_getter(where=self.where())
        argument_list = self.list_visible_asset_filesystem_paths(head=head)
        space_delimited_lowercase_asset_class_name = stringtools.string_to_space_delimited_lowercase(
            self.asset_class.__name__)
        plural_space_delimited_lowercase_asset_class_name = stringtools.pluralize_string(
            space_delimited_lowercase_asset_class_name)
        getter.append_argument_range(plural_space_delimited_lowercase_asset_class_name, argument_list)
        result = getter.run()
        if self.session.backtrack():
            return
        asset_indices = [asset_number - 1 for asset_number in result]
        total_assets_removed = 0
        for asset_number in result:
            asset_index = asset_number - 1
            asset_filesystem_path = argument_list[asset_index]
            asset_proxy = self.get_asset_proxy(asset_filesystem_path)
            asset_proxy.remove()
            total_assets_removed += 1
        self.io.proceed('{} asset(s) removed.'.format(total_assets_removed))

    # TODO: write test
    def rename_asset_interactively(self, head=None):
        self.session.push_backtrack()
        asset_package_path = self.select_asset_package_path_interactively(
            head=head, infinitival_phrase='to rename')
        self.session.pop_backtrack()
        if self.session.backtrack():
            return
        asset_proxy = self.get_asset_proxy(asset_package_path)
        asset_proxy.rename_interactively()

    def run(self, cache=False, clear=True, head=None, rollback=None, user_input=None):
        self.io.assign_user_input(user_input=user_input)
        breadcrumb = self.session.pop_breadcrumb(rollback=rollback)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self.breadcrumb)
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)
        self.session.restore_breadcrumbs(cache=cache)

    def select_asset_package_path_interactively(
        self, clear=True, cache=False, head=None, infinitival_phrase=None, user_input=None):
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(self.make_asset_selection_breadcrumb(infinitival_phrase=infinitival_phrase))
            menu = self.make_asset_selection_menu(head=head)
            result = menu.run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            else:
                break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        return result

    def strip_file_extension_from_file_name(self, file_name):
        if '.' in file_name:
            return file_name[:file_name.rindex('.')]
        return file_name

    def svn_add(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_add(is_interactive=False)
        self.io.proceed(is_interactive=is_interactive)

    def svn_ci(self, is_interactive=True):
        getter = self.io.make_getter(where=self.where())
        getter.append_string('commit message')
        commit_message = getter.run()
        if self.session.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.io.display(line)
        if not self.io.confirm():
            return
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_ci(commit_message=commit_message, is_interactive=False)
        self.io.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_st(is_interactive=False)
        self.io.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_up(is_interactive=False)
        self.io.proceed(is_interactive=is_interactive)

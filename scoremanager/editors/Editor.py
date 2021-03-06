# -*- encoding: utf-8 -*-
import types
from abjad.tools import stringtools
from scoremanager.core.Controller import Controller


class Editor(Controller):
    r'''Editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attributes_in_memory',
        '_explicit_breadcrumb',
        '_is_autoadding',
        '_is_autoadvancing',
        '_is_autostarting',
        '_target',
        '__target_class',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        session=None, 
        target=None,
        explicit_breadcrumb=None,
        is_autoadding=False,
        is_autoadvancing=False,
        is_autostarting=False,
        ):
        Controller.__init__(self, session=session)
        self._attributes_in_memory = {}
        self._explicit_breadcrumb = None
        self._is_autoadding = is_autoadding
        self._is_autoadvancing = is_autoadvancing
        self._is_autostarting = is_autostarting
        if type(self).__name__ == 'Editor':
            self.__target_class = None
        else:
            target_manifest = self._target_manifest
            if not target_manifest:
                message = 'can not find target manifest for {!r}.'
                message = message.format(self)
                raise Exception(message)
        if target is not None:
            assert isinstance(target, self._target_class)
        self._target = target

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of editor.

        Returns string.
        '''
        if self.target is None:
            summary = ''
        else:
            class_name = type(self.target).__name__
            summary = 'target={}'.format(class_name)
        return '<{}({})>'.format(type(self).__name__, summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self.explicit_breadcrumb:
            return self.explicit_breadcrumb
        elif self._target_name:
            return self._target_name
        else:
            class_name = self._target_class.__name__
            return stringtools.string_to_space_delimited_lowercase(class_name)

    @property
    def _target_class(self):
        return self._target_manifest._target_class

    @property
    def _target_manifest(self):
        target_class = self.__target_class
        dummy_target = target_class()
        target_manifest = getattr(dummy_target, '_target_manifest')
        return target_manifest

    @property
    def _target_name(self):
        target_name_attribute = self._target_manifest.target_name_attribute
        if target_name_attribute:
            return getattr(
                self.target, 
                self._target_manifest.target_name_attribute, 
                None,
                )

    @property
    def _target_summary_lines(self):
        result = []
        if self.target is not None:
            target_attribute_names = []
            if hasattr(self, '_target_manifest'):
                names = self._target_manifest.attribute_names
                target_attribute_names.extend(names)
            for target_attribute_name in target_attribute_names:
                name = stringtools.string_to_space_delimited_lowercase(
                    target_attribute_name)
                value = self._io_manager._get_one_line_menu_summary(
                    getattr(self.target, target_attribute_name))
                result.append('{}: {}'.format(name, value))
        return result

    ### PRIVATE METHODS ###

    def _attribute_name_to_menu_key(self, attribute_name, menu_keys):
        found_menu_key = False
        attribute_parts = attribute_name.split('_')
        i = 1
        while True:
            menu_key = ''.join([part[:i] for part in attribute_parts])
            if menu_key not in menu_keys:
                break
            i = i + 1
        return menu_key

    def _clean_up_attributes_in_memory(self):
        if self.target is None:
            try:
                self._initialize_target_from_attributes_in_memory()
            except ValueError:
                pass
        self._attributes_in_memory = {}

    def _copy_target_attributes_to_memory(self):
        self._attributes_in_memory = {}
        retrievable_attribute_names = []
        if hasattr(self, '_target_manifest'):
            names = self._target_manifest.positional_initializer_retrievable_attribute_names
            retrievable_attribute_names.extend(names)
        for attribute_name in retrievable_attribute_names:
            attribute_value = getattr(self.target, attribute_name, None)
            if attribute_value is not None:
                attribute_name = \
                    self._target_manifest._to_initializer_argument_names(
                    attribute_name)
                self._attributes_in_memory[attribute_name] = attribute_value
        keyword_attribute_names = []
        if hasattr(self, '_target_manifest'):
            names = self._target_manifest.keyword_attribute_names
            keyword_attribute_names.extend(names)
        for attribute_name in keyword_attribute_names:
            attribute_value = getattr(self.target, attribute_name, None)
            if attribute_value is not None:
                self._attributes_in_memory[attribute_name] = attribute_value
        self._target = None

    def _edit(self, target_class):
        self.__target_class = target_class
        self._run()

    def _get_editor(
        self, 
        attribute_detail,
        space_delimited_attribute_name, 
        prepopulated_value, 
        **kwargs
        ):
        from scoremanager import iotools
        from scoremanager import wizards
        editor_callable = attribute_detail.editor_callable
        if (
            isinstance(editor_callable, types.FunctionType) and
            editor_callable.__name__.startswith('make_')
            ):
            editor = editor_callable(session=session, **kwargs)
        elif isinstance(editor_callable, types.FunctionType):
            editor = editor_callable(
                space_delimited_attribute_name,
                session=self._session, 
                prepopulated_value=prepopulated_value, 
                allow_none=attribute_detail.allow_none, 
                **kwargs
                )
        elif issubclass(editor_callable, Editor):
            editor = editor_callable(
                session=self._session, 
                target=prepopulated_value, 
                **kwargs
                )
        elif issubclass(editor_callable, iotools.Selector):
            editor = editor_callable(session=self._session, **kwargs)
        elif issubclass(editor_callable, wizards.Wizard):
            editor = editor_callable(
                session=self._session, 
                target=prepopulated_value, 
                **kwargs
                )
        else:
            message = 'what is {!r}?'
            message = message.format(editor_callable)
            raise ValueError(message)
        return editor

    def _handle_main_menu_result(self, result):
        if result == 'user entered lone return':
            self._session._is_backtracking_locally = True
            return
        attribute_name = self._target_manifest._menu_key_to_attribute_name(
            result)
        prepopulated_value = self._menu_key_to_prepopulated_value(result)
        kwargs = self._menu_key_to_delegated_editor_kwargs(result)
        editor = self._menu_key_to_editor(
            result, 
            session=self._session, 
            prepopulated_value=prepopulated_value, 
            **kwargs
            )
        if editor is not None:
            result = editor._run()
            if self._should_backtrack():
                # TODO: maybe this should be in a context manager
                self._is_autoadvancing = False
                return
            if hasattr(editor, 'target'):
                attribute_value = editor.target
            else:
                attribute_value = result
            self._set_target_attribute(attribute_name, attribute_value)

    def _initialize_target(self):
        if self.target is not None:
            return
        else:
            self._target = self._target_class()

    def _initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        positional_argument_names = []
        if hasattr(self, '_target_manifest'):
            names = self._target_manifest.positional_initializer_argument_names
            positional_argument_names.extend(names)
        for attribute_name in positional_argument_names:
            if attribute_name in self._attributes_in_memory:
                args.append(self._attributes_in_memory.get(attribute_name))
        keyword_attribute_names = []
        if hasattr(self, '_target_manifest'):
            names = self._target_manifest.keyword_attribute_names
            keyword_attribute_names.extend(names)
        for attribute_name in keyword_attribute_names:
            if attribute_name in self._attributes_in_memory:
                kwargs[attribute_name] = \
                    self._attributes_in_memory.get(attribute_name)
        self._target = self._target_class(*args, **kwargs)

    def _make_main_menu(self, name='editor'):
        menu = self._io_manager.make_menu(
            where=self._where,
            name=name,
            )
        menu_entries = self._make_target_attribute_tokens()
        if menu_entries:
            keyed_attribute_section = menu.make_keyed_attribute_section(
                name='keyed attributes',
                is_numbered=True,
                ) 
            for menu_entry in menu_entries:
                keyed_attribute_section.append(menu_entry)
        self._make_done_menu_section(menu)
        return menu

    def _make_target_attribute_tokens(self):
        result = []
        for attribute_detail in self._target_manifest.attribute_details:
            if attribute_detail.is_null:
                result.append(())
                continue
            key = attribute_detail.menu_key
            display_string = attribute_detail._space_delimited_lowercase_name
            if self.target is not None:
                attribute_value = getattr(
                    self.target, attribute_detail.retrievable_name, None)
                if attribute_value is None:
                    attribute_value = getattr(
                        self.target, attribute_detail.name, None)
            else:
                attribute_value = self._attributes_in_memory.get(
                    attribute_detail.retrievable_name)
                if attribute_value is None:
                    attribute_value = self._attributes_in_memory.get(
                        attribute_detail.name)
            if hasattr(attribute_value, '__len__') and \
                not len(attribute_value):
                attribute_value = None
            prepopulated_value = self._io_manager._get_one_line_menu_summary(
                attribute_value)
            menu_entry = (display_string, key, prepopulated_value)
            result.append(menu_entry)
        return result

    def _menu_key_to_delegated_editor_kwargs(self, menu_key):
        return {}

    def _menu_key_to_editor(
        self, 
        menu_key, 
        prepopulated_value, 
        session=None, 
        **kwargs
        ):
        manifest = self._target_manifest
        assert manifest
        attribute_name = manifest._menu_key_to_attribute_name(menu_key)
        attribute_name = attribute_name.replace('_', ' ')
        attribute_detail = manifest._menu_key_to_attribute_detail(menu_key)
        editor = self._get_editor(
            attribute_detail,
            attribute_name,
            prepopulated_value,
            **kwargs
            )
        return editor

    def _menu_key_to_prepopulated_value(self, menu_key):
        attribute_name = \
            self._target_manifest._menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(
            controller=self,
            on_exit_callbacks=(self._clean_up_attributes_in_memory,),
            )
        with context:
            self._initialize_target()
            if self._should_backtrack():
                return
            result = None
            entry_point = None
            is_first_pass = True
            while True:
                if self._is_autoadding:
                    menu = self._make_main_menu()
                    result = 'add'
                    menu._predetermined_user_input = result
                    menu._run()
                    is_first_pass = False
                elif is_first_pass and self._is_autostarting:
                    menu = self._make_main_menu()
                    result = menu._get_first_nonhidden_return_value_in_menu()
                    menu._predetermined_user_input = result
                    menu._run()
                    is_first_pass = False
                elif result and self._is_autoadvancing:
                    entry_point = entry_point or result
                    result = \
                        menu._return_value_to_next_return_value_in_section(
                            result)
                    if result == entry_point:
                        self._is_autoadvancing = False
                        continue
                else:
                    menu = self._make_main_menu()
                    result = menu._run()
                    if self._should_backtrack():
                        return
                    elif not result:
                        continue
                if result == 'done':
                    break
                self._handle_main_menu_result(result)
                if self._should_backtrack():
                    return

    def _set_target_attribute(self, attribute_name, attribute_value):
        if self.target is not None:
            if not self._session.is_complete:
                # if the attribute is read / write
                try:
                    setattr(self.target, attribute_name, attribute_value)
                # elif the attribute is read only
                except AttributeError:
                    self._copy_target_attributes_to_memory()
                    self._attributes_in_memory[attribute_name] = attribute_value
        else:
            self._attributes_in_memory[attribute_name] = attribute_value

    def _target_args_to_target_summary_lines(self, target):
        result = []
        for arg in getattr(target, 'args', []):
            name = stringtools.string_to_space_delimited_lowercase(arg)
            attribute = getattr(target, arg)
            value = self._io_manager._get_one_line_menu_summary(attribute)
            result.append('{}: {}'.format(name, value))
        return result

    def _target_kwargs_to_target_summary_lines(self, target):
        result = []
        for kwarg in getattr(target, 'kwargs', []):
            name = stringtools.string_to_space_delimited_lowercase(kwarg)
            value = self._io_manager._get_one_line_menu_summary(
                getattr(target, kwarg))
            result.append('{}: {}'.format(name, value))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def explicit_breadcrumb(self):
        r'''Gets editor explicit breadcrumb.

        Returns string or none.
        '''
        return self._explicit_breadcrumb

    @property
    def is_autoadding(self):
        r'''Is true when editor is autoadding. Otherwise false.

        Returns boolean.
        '''
        return self._is_autoadding

    @property
    def is_autoadvancing(self):
        r'''Is true when editor is autoadvancing. Otherwise false.

        Returns boolean.
        '''
        return self._is_autoadvancing

    @property
    def is_autostarting(self):
        r'''Is true when editor is autostarting. Otherwise false.

        Returns boolean.
        '''
        return self._is_autostarting

    @property
    def target(self):
        r'''Gets editor target.

        Returns object or none.
        '''
        return self._target
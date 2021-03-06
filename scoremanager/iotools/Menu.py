# -*- encoding: utf-8 -*-
import os
import textwrap
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Menu(ScoreManagerObject):
    r'''Menu.

    ..  container:: example

        ::

            >>> menu = scoremanager.iotools.Menu(
            ...     include_default_hidden_sections=False,
            ...     )
            >>> section = menu.make_command_section(name='test')
            >>> entry = section.append(('foo - add', 'add'))
            >>> entry = section.append(('foo - delete', 'delete'))
            >>> entry = section.append(('foo - modify', 'modify'))

        ::

            >>> menu
            <Menu (1)>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_section',
        '_breadcrumb_callback',
        '_client_source_code_location',
        '_hide_current_run',
        '_menu_sections',
        '_name',
        '_predetermined_user_input',
        '_should_clear_terminal',
        '_title',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        session=None, 
        where=None,
        breadcrumb_callback=None,
        # TODO: maybe remove include_default_hidden_sections?
        include_default_hidden_sections=False,
        name=None,
        title=None,
        ):
        ScoreManagerObject.__init__(self, session=session)
        self._breadcrumb_callback = breadcrumb_callback
        self._client_source_code_location = where
        self._menu_sections = []
        if include_default_hidden_sections:
            self._make_default_hidden_sections()
        self._name = name
        self._predetermined_user_input = None
        self._should_clear_terminal = False
        self._title = title

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets menu section with name equal to `expr`.

        Raises key error when no menu section with name equal to `expr` is
        found in menu.

        Returns menu section.
        '''
        assert isinstance(expr, str)
        for menu_section in self.menu_sections:
            if menu_section.name == expr:
                return menu_section
        raise KeyError(expr)

    def __len__(self):
        r'''Gets number of menu sections in menu.

        Returns nonnegative integer.
        '''
        return len(self.menu_sections)

    def __repr__(self):
        r'''Gets interpreter representation of menu.

        Returns string.
        '''
        if self.name:
            string = '<{} {!r} ({})>'
            string = string.format(type(self).__name__, self.name, len(self))
        else:
            string = '<{} ({})>'
            string = string.format(type(self).__name__, len(self))
        return string

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._breadcrumb_callback == 'name':
            return self.name
        elif self._breadcrumb_callback:
            return self._breadcrumb_callback()

    ### PRIVATE METHODS ###

    def _change_user_input_to_directive(self, user_input):
        user_input = stringtools.strip_diacritics_from_binary_string(
            user_input)
        if self._user_enters_nothing(user_input):
            default_value = None
            for menu_section in self.menu_sections:
                if menu_section._has_default_value:
                    default_value = menu_section._default_value
            if default_value is not None:
                return self._enclose_in_list(default_value)
        elif user_input in ('s', 'h', 'q', 'b', 'n', '?', 'r'):
            return user_input
        elif user_input.startswith('!'):
            return user_input
        for menu_section in self.menu_sections:
            for menu_entry in menu_section.menu_entries:
                if menu_entry.matches(user_input):
                    return self._enclose_in_list(menu_entry.return_value)
        for menu_section in self.menu_sections:
            for menu_entry in menu_section.menu_entries:
                if menu_entry.matches(user_input.lower()):
                    return self._enclose_in_list(menu_entry.return_value)
        if self._user_enters_argument_range(user_input):
            return self._handle_argument_range_user_input(user_input)

    def _clear_terminal(self):
        if self._should_clear_terminal:
            self._io_manager.clear_terminal()

    def _display(self):
        from scoremanager import iotools
        context = iotools.SourceCodeContext(self)
        with context:
            self._clear_terminal()
            if not self._session.hide_hidden_commands:
                self._display_all_commands()
            menu_lines = self._make_menu_lines()
            self._io_manager.display(
                menu_lines,
                capitalize_first_character=False,
                )
            user_entered_lone_return = False
            user_input = self._io_manager.handle_user_input('')
            if user_input == '':
                user_entered_lone_return = True
            directive = self._change_user_input_to_directive(user_input)
            directive = self._strip_default_notice_from_strings(directive)
            self._session._hide_next_redraw = False
            directive = self._io_manager._handle_directive(directive)
            if directive is None and user_entered_lone_return:
                result = 'user entered lone return'
            elif directive is None and not user_entered_lone_return:
                result = None
            else:
                result = directive
            return result

    def _display_all_commands(self):
        menu_lines = []
        for menu_section in self.menu_sections:
            #print repr(menu_section), 'SECTION'
            if not menu_section.is_command_section:
                continue
            for menu_entry in menu_section.menu_entries:
                key = menu_entry.key
                display_string = menu_entry.display_string
                menu_line = self._make_tab(1)
                menu_line += '{} ({})'.format(display_string, key)
                menu_lines.append(menu_line)
            menu_lines.append('')
        if menu_lines:
            menu_lines.pop()
        menu_lines = self._make_bicolumnar(menu_lines)
        title = self._session.menu_header
        title = stringtools.capitalize_string_start(title)
        menu_lines[0:0] = [title, '']
        menu_lines.append('')
        self._clear_terminal()
        self._io_manager.display(
            menu_lines, 
            capitalize_first_character=False,
            )
        self._session._hide_hidden_commands = True
        self._session._hide_next_redraw = True

    def _enclose_in_list(self, expr):
        if self._has_ranged_section():
            return [expr]
        else:
            return expr

    def _get_first_nonhidden_return_value_in_menu(self):
        for menu_section in self.menu_sections:
            if menu_section.is_hidden:
                continue
            if menu_section._menu_entry_return_values:
                return menu_section._menu_entry_return_values[0]

    def _handle_argument_range_user_input(self, user_input):
        if not self._has_ranged_section():
            return
        for menu_section in self.menu_sections:
            if menu_section.is_ranged:
                ranged_section = menu_section
        entry_numbers = ranged_section._argument_range_string_to_numbers(
            user_input)
        if not entry_numbers:
            return
        entry_indices = [entry_number - 1 for entry_number in entry_numbers]
        result = []
        for i in entry_indices:
            entry = ranged_section._menu_entry_return_values[i]
            result.append(entry)
        return result

    def _has_numbered_section(self):
        return any(x.is_numbered for x in self.menu_sections)

    def _has_ranged_section(self):
        return any(x.is_ranged for x in self.menu_sections)

    def _make_bicolumnar(self, lines):
        terminal_height = 50
        column_width = 55
        if len(lines) < terminal_height:
            return lines
        if 2 * terminal_height < len(lines):
            message = 'too many lines to lay out in two columns: {!r}.'
            message = message.format(len(lines))
            raise ValueError(message)
        split_lines = []
        for line in lines:
            line = line.strip()
            if column_width < len(line):
                width = column_width - 6
                new_lines = textwrap.wrap(line, width=width)
                tab_string = self._make_tab(1)
                split_lines.append(tab_string + new_lines[0])
                for new_line in new_lines[1:]:
                    split_lines.append(5 * ' ' + new_line)
            elif line == '':
                split_lines.append(line)
            else:
                tab_string = self._make_tab(1)
                split_lines.append(tab_string + line)
        lines = split_lines
        left_column_lines = lines[:terminal_height]
        for i, line in enumerate(reversed(left_column_lines)):
            if line == '':
                break
        terminal_height -= i
        left_column_lines = lines[:terminal_height-1]
        right_column_lines = lines[terminal_height:]
        pair = (left_column_lines, right_column_lines)
        generator = sequencetools.zip_sequences(pair, truncate=False)
        massaged_lines = []
        for element in generator:
            if len(element) == 2:
                left_line, right_line = element
                left_line = left_line.rstrip()
                extra_count = column_width - len(left_line)
                extra_space = extra_count * ' '
                left_line = left_line + extra_space
                right_line = right_line.strip()
            else:
                assert len(element) == 1
                left_line = element[0]
                right_line = ''
            massaged_line = left_line + right_line
            massaged_lines.append(massaged_line)
        return massaged_lines

    def _make_commands_menu_section(self):
        section = self.make_command_section(name='commands', is_hidden=True)
        section.append(('commands - all', '?'))

    def _make_default_hidden_sections(self):
        sections = []
        sections.append(self._make_commands_menu_section())
        if self._session.is_in_score:
            sections.append(self._make_edit_menu_section())
        sections.append(self._make_go_menu_section())
        sections.append(self._make_lilypond_menu_section())
        sections.append(self._make_python_menu_section())
        sections.append(self._make_repository_menu_section())
        sections.append(self._make_go_wranglers_menu_section())
        sections.append(self._make_go_scores_menu_section())
        sections.append(self._make_session_menu_section())
        sections.append(self._make_source_code_menu_section())
        sections.append(self._make_system_menu_section())
        return sections

    def _make_edit_menu_section(self):
        section = self.make_command_section(
            name='edit',
            is_hidden=True,
            )
        section.append(('edit - current stylesheet', 'Y'))
        return section

    def _make_go_menu_section(self):
        section = self.make_command_section(
            name='go', 
            is_hidden=True,
            )
        section.append(('go - back', 'b'))
        section.append(('go - home', 'h'))
        section.append(('go - score', 's'))
        return section

    def _make_go_scores_menu_section(self):
        section = self.make_command_section(
            name='go - scores',
            is_alphabetized=False,
            is_hidden=True,
            )
        section.append(('go - next score', '>>'))
        section.append(('go - previous score', '<<'))
        return section

    def _make_go_wranglers_menu_section(self):
        section = self.make_command_section(
            name='go - wranglers',
            is_hidden=True,
            )
        section.append(('go - build', 'u'))
        section.append(('go - distribution', 'd'))
        section.append(('go - makers', 'k'))
        section.append(('go - materials', 'm'))
        section.append(('go - segments', 'g'))
        if self._session.is_in_score:
            section.append(('go - setup', 'p'))
        section.append(('go - stylesheets', 'y'))
        return section

    def _make_lilypond_menu_section(self):
        section = self.make_command_section(name='lilypond', is_hidden=True)
        section.append(('LilyPond log - read only', 'llro'))
        return section

    def _make_menu_lines(self):
        result = []
        if not self.name:
            message = '{!r} has no name.'
            message = message.format(self)
            raise Exception(message)
        result.extend(self._make_title_lines())
        result.extend(self._make_section_lines())
        return result

    def _make_python_menu_section(self):
        section = self.make_command_section(
            name='python', 
            is_hidden=True,
            match_on_display_string=False,
            )
        section.append(('Python - doctest', 'pyd'))
        section.append(('Python - invoke', 'pyi'))
        section.append(('Python - test', 'pyt'))
        return section

    def _make_repository_menu_section(self):
        section = self.make_command_section(
            name='repository', 
            is_hidden=True,
            )
        section.append(('repository - add', 'rad'))
        section.append(('repository - commit', 'rci'))
        section.append(('repository - revert', 'rrv'))
        section.append(('repository - status', 'rst'))
        section.append(('repository - update', 'rup'))
        return section

    def _make_section(
        self, 
        is_alphabetized=False,
        is_asset_section=False,
        is_attribute_section=False,
        is_command_section=False,
        is_hidden=False, 
        is_informational_section=False,
        is_material_summary_section=False,
        is_navigation_section=False,
        is_numbered=False, 
        is_ranged=False, 
        display_prepopulated_values=False,
        default_index=None,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        return_value_attribute='display_string',
        title=None,
        ):
        from scoremanager import iotools
        assert not (is_numbered and self._has_numbered_section())
        assert not (is_ranged and self._has_ranged_section())
        menu_section = iotools.MenuSection(
            is_alphabetized=is_alphabetized,
            is_asset_section=is_asset_section,
            is_attribute_section=is_attribute_section,
            is_command_section=is_command_section,
            is_hidden=is_hidden,
            is_informational_section=is_informational_section,
            is_material_summary_section=is_material_summary_section,
            is_navigation_section=is_navigation_section,
            is_numbered=is_numbered,
            is_ranged=is_ranged,
            display_prepopulated_values=display_prepopulated_values,
            default_index=default_index,
            match_on_display_string=match_on_display_string,
            menu_entries=menu_entries,
            name=name,
            return_value_attribute=return_value_attribute,
            title=title,
            )
        self.menu_sections.append(menu_section)
        self.menu_sections.sort(key=lambda x: x.name)
        noncommand_sections = [
            x for x in self.menu_sections
            if (not x.is_command_section and not x.is_navigation_section)
            ]
        for noncommand_section in noncommand_sections:
            self.menu_sections.remove(noncommand_section)
        for noncommand_section in noncommand_sections:
            self.menu_sections.insert(0, noncommand_section)
        return menu_section

    def _make_section_lines(self):
        result = []
        section_names = []
        for menu_section in self.menu_sections:
            if not len(menu_section):
                message = '{!r} contains {!r}.'
                message = message.format(self, menu_section)
                raise Exception(message)
            if not menu_section.name:
                message = '{!r} contains {!r}.'
                message = message.format(self, menu_section)
                raise Exception(message)
            if menu_section.name in section_names:
                message = '{!r} with duplicate section: {!r}.'
                message = message.format(self, menu_section)
                raise Exception(message)
            else:
                section_names.append(menu_section.name)
            hide = self._session.hide_hidden_commands
            if hide and menu_section.is_hidden:
                continue
            section_menu_lines = menu_section._make_menu_lines()
            result.extend(section_menu_lines)
        if self._hide_current_run:
            result = []
        return result

    def _make_session_menu_section(self):
        section = self.make_command_section(name='session', is_hidden=True)
        section.append(('session - display variables', 'sdv'))

    def _make_source_code_menu_section(self):
        section = self.make_command_section(
            name='source code',
            is_hidden=True,
            )
        section.append(('source code - edit', 'sce'))
        section.append(('source code - location', 'scl'))
        return section

    def _make_system_menu_section(self):
        section = self.make_command_section(name='system', is_hidden=True)
        section.append(('system - quit', 'q'))
        section.append(('system - shell', '!'))
        return section

    def _make_tab(self, n=1):
        return 4 * n * ' '

    def _make_title_lines(self):
        result = []
        if not self._hide_current_run:
            if self.title is not None:
                title = self.title
            else:
                title = self._session.menu_header
            result.append(stringtools.capitalize_string_start(title))
            result.append('')
        return result

    def _return_value_to_location_pair(self, return_value):
        for i, menu_section in enumerate(self.menu_sections):
            if return_value in menu_section._menu_entry_return_values:
                j = menu_section._menu_entry_return_values.index(return_value)
                return i, j

    def _return_value_to_next_return_value_in_section(self, return_value):
        section_index, entry_index = self._return_value_to_location_pair(
            return_value)
        menu_section = self.menu_sections[section_index]
        entry_index = (entry_index + 1) % len(menu_section)
        return menu_section._menu_entry_return_values[entry_index]

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        clear_terminal, hide_current_run = True, False
        context = iotools.ControllerContext(
            self,
            reset_hide_hidden_commands=False,
            )
        with context:
            while True:
                self._should_clear_terminal = clear_terminal
                self._hide_current_run = hide_current_run
                clear_terminal, hide_current_run = False, True
                result = self._predetermined_user_input
                if not result:
                    result = self._display()
                if self._session.is_complete:
                    return result
                if result == 'r':
                    clear_terminal, hide_current_run = True, False
                else:
                    return result

    # TODO: apply default notice at display time 
    #       so this can be completely removed
    def _strip_default_notice_from_strings(self, expr):
        if isinstance(expr, list):
            cleaned_list = []
            for element in expr:
                if element.endswith(' (default)'):
                    element = element.replace(' (default)', '')
                cleaned_list.append(element)
            return cleaned_list
        elif isinstance(expr, str):
            if expr.endswith(' (default)'):
                expr = expr.replace(' (default)', '')
            return expr
        else:
            return expr

    def _user_enters_argument_range(self, user_input):
        if ',' in user_input:
            return True
        if '-' in user_input:
            return True
        return False

    def _user_enters_nothing(self, user_input):
        return not user_input or (3 <= len(user_input) and \
            'default'.startswith(user_input))

    ### PUBLIC PROPERTIES ###

    @property
    def menu_sections(self):
        r'''Gets menu sections.

        ..  container:: example

            ::

                >>> for menu_section in menu.menu_sections:
                ...     menu_section
                <MenuSection 'test' (3)>

        Returns list.
        '''
        return self._menu_sections

    @property
    def name(self):
        r'''Gets menu name.

        ..  container:: example

            ::

                >>> menu.name is None
                True

        Returns list.
        '''
        return self._name

    @property
    def title(self):
        r'''Gets menu title.

        ..  container:: example

            ::

                >>> menu.title is None
                True

        Returns string or none.
        '''
        return self._title

    ### PUBLIC METHODS ###

    def make_asset_section(
        self, 
        menu_entries=None, 
        name='assets',
        ):
        r'''Makes asset section.

        With these attributes:

            * is asset section
            * is numbered
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            is_asset_section=True,
            is_numbered=True,
            name=name,
            return_value_attribute='explicit',
            )
        return section

    def make_attribute_section(self, menu_entries=None, name=None, title=None):
        r'''Makes attribute section.

        With these attributes:

            * is attribute section
            * is numbered
            * displays prepopulated values
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            display_prepopulated_values=True,
            is_attribute_section=True,
            is_numbered=True,
            return_value_attribute='explicit',
            name=name,
            title=title,
            )
        return section

    def make_command_section(
        self,
        is_alphabetized=True,
        is_hidden=False,
        default_index=None,
        match_on_display_string=False,
        menu_entries=None,
        name=None,
        ):
        r'''Makes command section.

        Menu section with these attributes:

            * is command section
            * is alphabetized
            * is not hidden
            * does NOT match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_alphabetized=is_alphabetized,
            is_command_section=True,
            is_hidden=is_hidden,
            default_index=default_index,
            match_on_display_string=match_on_display_string,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_informational_section(
        self,
        menu_entries=None,
        name='information',
        ):
        r'''Makes informational section.

        Menu section with these attributes:

            * is informational section
            * not hidden
            * does not match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_hidden=False,
            is_informational_section=True,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_keyed_attribute_section(
        self, 
        is_numbered=False, 
        menu_entries=None,
        name=None,
        ):
        r'''Makes keyed attribute section.

        With these attributes:

            * not numbered

        Returns menu section.
        '''
        section = self._make_section(
            display_prepopulated_values=True,
            is_numbered=is_numbered,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_material_summary_section(
        self, 
        menu_entries=None, 
        name='material summary',
        ):
        r'''Makes asset section.

        With these attributes:

            * is material summary section
            * is not numbered
            * return value set to explicit

        Returns menu section.
        '''
        section = self._make_section(
            is_material_summary_section=True,
            is_numbered=False,
            name=name,
            return_value_attribute='explicit',
            )
        return section

    def make_navigation_section(
        self,
        is_hidden=False,
        match_on_display_string=True,
        menu_entries=None,
        name=None,
        ):
        r'''Makes navigation section.

        Menu section with these attributes:

            * is navigation section
            * not hidden
            * match on display string
            * return value attribute equal to ``'key'``

        Returns menu section.
        '''
        section = self._make_section(
            is_hidden=is_hidden,
            is_navigation_section=True,
            match_on_display_string=match_on_display_string,
            name=name,
            return_value_attribute='key',
            )
        return section

    def make_numbered_list_section(
        self, 
        menu_entries=None, 
        name=None,
        title=None,
        default_index=None,
        ):
        r'''Makes numbered list section.

        With these attributes:

            * asset section
            * numbered
            * ranged
            * return value equal to display string

        Returns menu section.
        '''
        section = self._make_section(
            is_asset_section=True,
            is_numbered=True,
            is_ranged=True,
            default_index=default_index,
            name=name,
            return_value_attribute='display_string',
            title=title,
            )
        return section

    def make_numbered_section(self, menu_entries=None, name=None):
        r'''Makes numbered section.

        With these attributes:

            * asset section
            * numbered
            * return value equal to item number

        Returns menu section.
        '''
        section = self._make_section(
            name=name,
            is_asset_section=True,
            is_numbered=True,
            return_value_attribute='number',
            )
        return section
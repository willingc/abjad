import types
from abjad.tools import stringtools
from experimental.tools.scoremanagertools import predicates
from experimental.tools.scoremanagertools.core.ScoreManagerObject \
    import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.Menu import Menu
from experimental.tools.scoremanagertools.menuing.PromptMakerMixin \
    import PromptMakerMixin


class UserInputGetter(ScoreManagerObject, PromptMakerMixin):
    '''User input getter menu.

    .. note:: add docstring.

    Return user input getter.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, where=None):
        ScoreManagerObject.__init__(self, session=session)
        PromptMakerMixin.__init__(self)
        hidden_section = self._io.make_default_hidden_section()
        self._prompts = []
        self.allow_none = False
        self.capitalize_prompts = True
        self.include_newlines = False
        self.number_prompts = False
        self.prompt_character = '>'
        self.where=where

    ### SPECIAL METHODS ###

    def __len__(self):
        '''Number of prompts in user input getter menu.

        Return nonnegative integer.
        '''
        return len(self.prompts)
        
    def __repr__(self):
        '''Interpreter representation of user input getter.

        Return string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _current_prompt(self):
        return self.prompts[self._prompt_index]

    ### PRIVATE METHODS ###

    def _display_help(self):
        lines = []
        lines.append(self._current_prompt.help_string)
        lines.append('')
        self._io.display(lines)

    def _evaluate_user_input(self, user_input):
        target_menu_section = self._current_prompt.target_menu_section
        setup_statements = self._current_prompt.setup_statements
        if self.allow_none and user_input in ('', 'None'):
            evaluated_user_input = None
        elif target_menu_section is not None:
            evaluated_user_input = \
                target_menu_section._argument_range_string_to_numbers(
                user_input)
        elif setup_statements:
            for setup_statement in self._current_prompt.setup_statements:
                try:
                    command = setup_statement.format(user_input)
                    exec(command)
                    continue
                except (NameError, SyntaxError):
                    pass
                try:
                    command = setup_statement.format(repr(user_input))
                    exec(command)
                except ValueError:
                    self._display_help()
        else:
            try:
                evaluated_user_input = eval(user_input)
            except (NameError, SyntaxError):
                evaluated_user_input = user_input
        if not 'evaluated_user_input' in locals():
            return
        if not self._validate_evaluated_user_input(evaluated_user_input):
            self._display_help()
            return
        self._evaluated_user_input.append(evaluated_user_input)
        self._prompt_index += 1
        self._current_prompt_is_done = True

    def _handle_hidden_menu_section_return_value(self, directive):
        if isinstance(directive, list) and len(directive) == 1:
            key = directive[0]
        else:
            key = directive
        if key in ('b', 'back'):
            self._session.is_backtracking_locally = True
        elif key == 'cmds':
            self.toggle_menu_commands()
        elif key == 'exec':
            self.interactively_exec_statement()
        elif key == 'grep':
            self.interactively_grep_directories()
        elif key == 'here':
            self.interactively_edit_calling_code()
        elif key == 'hidden':
            self.display_hidden_menu_section()
        elif key == 'next':
            self._session.is_navigating_to_next_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key == 'prev':
            self._session.is_navigating_to_prev_score = True
            self._session.is_backtracking_to_score_manager = True
        elif key in ('q', 'quit'):
            self._session.user_specified_quit = True
#        # TODO: make this redraw!
#        elif key == 'r':
#            pass
        elif isinstance(key, str) and \
            3 <= len(key) and 'score'.startswith(key):
            if self._session.is_in_score:
                self._session.is_backtracking_to_score = True
        elif isinstance(key, str) and \
            3 <= len(key) and 'home'.startswith(key):
            self._session.is_backtracking_to_score_manager = True
        elif key == 'tw':
            self._session.enable_where = not self._session.enable_where
        elif key == 'where':
            self.display_calling_code_line_number()
        else:
            return directive

    def _indent_and_number_prompt_string(self, prompt_string):
        if self.number_prompts:
            prompt_number = self._prompt_index + 1
            prompt_string = '({}/{}) {}'.format(
                prompt_number, len(self), prompt_string)
        return prompt_string

    def _load_prompt_string(self):
        prompt_string = self._current_prompt.prompt_string
        if self.capitalize_prompts:
            prompt_string = stringtools.capitalize_string_start(prompt_string)
        self._prompt_strings.append(prompt_string)

    def _move_to_prev_prompt(self):
        self._evaluated_user_input.pop()
        self._prompt_index = self._prompt_index - 1

    def _present_prompt_and_evaluate_user_input(self, include_chevron=True):
        self._load_prompt_string()
        self._current_prompt_is_done = False
        while not self._current_prompt_is_done:
            prompt_string = self._prompt_strings[-1]
            prompt_string = self._indent_and_number_prompt_string(
                prompt_string)
            default_value = str(self._current_prompt.default_value)
            include_chevron = self._current_prompt.include_chevron
            user_input = self._io.handle_raw_input_with_default(
                prompt_string, 
                default_value=default_value,
                include_chevron=include_chevron, 
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character, 
                capitalize_prompt=self.capitalize_prompts)
            if user_input is None:
                self._prompt_index += 1
                break
            user_input = self._handle_hidden_menu_section_return_value(
                user_input)
            if self._session.backtrack():
                self._current_prompt_is_done = True
                self._all_prompts_are_done = True
            elif user_input is None:
                continue
            elif user_input == 'help':
                self._display_help()
            elif user_input == 'prev':
                self._move_to_prev_prompt()
                break
            elif user_input == 'skip':
                break
            elif isinstance(user_input, str):
                self._evaluate_user_input(user_input)
            else:
                self._io.print_not_yet_implemented()

    def _present_prompts_and_evaluate_user_input(self, include_chevron=True):
        self._io.clear_terminal()
        self._prompt_index = 0
        self._prompt_strings = []
        self._evaluated_user_input = []
        self._all_prompts_are_done = False
        while self._prompt_index < len(self) and \
            not self._all_prompts_are_done:
            self._present_prompt_and_evaluate_user_input(
                include_chevron=include_chevron)

    def _run(self, user_input=None, include_chevron=True):
        self._io.assign_user_input(user_input=user_input)
        with self.backtracking:
            self._present_prompts_and_evaluate_user_input(
                include_chevron=include_chevron)
        if len(self._evaluated_user_input) == 1:
            return self._evaluated_user_input[0]
        return self._evaluated_user_input[:]

    def _validate_evaluated_user_input(self, evaluated_user_input):
        if evaluated_user_input is None and self.allow_none:
            return True
        validation_function = self._current_prompt.validation_function
        return validation_function(evaluated_user_input)

    ### PUBLIC PROPERTIES ###

    @apply
    def allow_none():
        def fget(self):
            return self._allow_none
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._allow_none = expr
        return property(**locals())

    @apply
    def capitalize_prompts():
        def fget(self):
            return self._capitalize_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._capitalize_prompts = expr
        return property(**locals())

    @apply
    def include_newlines():
        def fget(self):
            return self._include_newlines
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._include_newlines = expr
        return property(**locals())

    @apply
    def number_prompts():
        def fget(self):
            return self._number_prompts
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._number_prompts = expr
        return property(**locals())

    @property
    def prompts(self):
        return self._prompts

    @apply
    def prompt_character():
        def fget(self):
            return self._prompt_character
        def fset(self, expr):
            assert isinstance(expr, str)
            self._prompt_character = expr
        return property(**locals())

    ### PUBLIC METHODS ###

    def interactively_exec_statement(self):
        self._io.interactively_exec_statement()
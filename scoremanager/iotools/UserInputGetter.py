# -*- encoding: utf-8 -*-
import types
from abjad.tools import stringtools
from scoremanager import predicates
from scoremanager.core.ScoreManagerObject import ScoreManagerObject
from scoremanager.iotools.PromptMakerMixin import PromptMakerMixin


class UserInputGetter(ScoreManagerObject, PromptMakerMixin):
    r'''User input getter.
    '''

    ### CLASS VARIABLES ###

    # multiple inheritance breaks slots
    __slots__ = (
        '_all_prompts_are_done',
        '_allow_none',
        '_capitalize_prompts',
        '_current_prompt_is_done',
        '_evaluated_user_input',
        '_include_newlines',
        '_include_chevron',
        '_number_prompts',
        '_prompt_character',
        '_prompt_index',
        '_prompt_strings',
        '_prompts',
        '_my_where'
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        session=None, 
        where=None,
        allow_none=False,
        capitalize_prompts=True,
        include_chevron=True,
        include_newlines=False,
        number_prompts=False,
        prompt_character='>',
        ):
        ScoreManagerObject.__init__(self, session=session)
        PromptMakerMixin.__init__(self)
        self._prompts = []
        self._allow_none = allow_none
        self._capitalize_prompts = capitalize_prompts
        self._include_chevron = include_chevron
        self._include_newlines = include_newlines
        self._number_prompts = number_prompts
        self._prompt_character = prompt_character
        self._my_where = where

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format of user input getter.

        Returns string.
        '''
        return repr(self)

    def __len__(self):
        r'''Gets number of prompts in user input getter menu.

        Returns nonnegative integer.
        '''
        return len(self.prompts)
        
    def __repr__(self):
        r'''Gets interpreter representation of user input getter.

        Returns string.
        '''
        return '<{} ({})>'.format(type(self).__name__, len(self))

    def __str__(self):
        r'''Gets string representation of user input getter.

        Returns string.
        '''
        return repr(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _current_prompt(self):
        return self.prompts[self._prompt_index]

    ### PRIVATE METHODS ###

    def _display_help(self):
        lines = []
        lines.append(self._current_prompt.help_string)
        lines.append('')
        self._io_manager.display(lines)

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

    def _move_to_previous_prompt(self):
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
            user_input = \
                self._io_manager.handle_user_input(
                prompt_string, 
                default_value=default_value,
                include_chevron=include_chevron, 
                include_newline=self.include_newlines,
                prompt_character=self.prompt_character, 
                capitalize_prompt=self.capitalize_prompts,
                )
            if user_input is None:
                self._prompt_index += 1
                break
            assert isinstance(user_input, str), repr(user_input)
            directive = self._io_manager._handle_directive(user_input)
            if self._should_backtrack():
                self._current_prompt_is_done = True
                self._all_prompts_are_done = True
            elif directive is None:
                continue
            elif directive == 'help':
                self._display_help()
            elif directive == 'previous':
                self._move_to_previous_prompt()
                break
            elif directive == 'skip':
                break
            elif isinstance(directive, str):
                self._evaluate_user_input(directive)
            else:
                self._io_manager.print_not_yet_implemented()

    def _present_prompts_and_evaluate_user_input(
        self, 
        include_chevron=True,
        ):
        self._prompt_index = 0
        self._prompt_strings = []
        self._evaluated_user_input = []
        self._all_prompts_are_done = False
        while self._prompt_index < len(self) and \
            not self._all_prompts_are_done:
            self._present_prompt_and_evaluate_user_input(
                include_chevron=include_chevron)

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        context = iotools.ControllerContext(
            controller=self,
            is_in_confirmation_environment=True,
            where=self.where,
            )
        with context:
            self._present_prompts_and_evaluate_user_input(
                include_chevron=self._include_chevron,
                )
            if len(self._evaluated_user_input) == 1:
                result = self._evaluated_user_input[0]
            else:
                result = self._evaluated_user_input[:]
            return result

    def _should_backtrack(self):
        if self._session.is_complete:
            return True
        elif self._session.is_backtracking_to_score_manager:
            return True
        # keep on backtracking ... do not consume this backtrack
        elif self._session.is_backtracking_locally:
            return True
        elif self._session.is_backtracking_to_score:
            return True
        elif self._session.is_autonavigating_within_score:
            return True
        else:
            return False

    def _validate_evaluated_user_input(self, evaluated_user_input):
        if evaluated_user_input is None and self.allow_none:
            return True
        validation_function = self._current_prompt.validation_function
        return validation_function(evaluated_user_input)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_none(self):
        r'''Is true when user input getter allows none.
        Otherwise false.

        Returns boolean.
        '''
        return self._allow_none

    @property
    def capitalize_prompts(self):
        r'''Is true when user input getter capitalizes prompts.
        Otherwise false.

        Returns boolean.
        '''
        return self._capitalize_prompts
        

    @property
    def include_newlines(self):
        r'''Is true when user input getter incldues newlines.
        Otherwise false.

        Returns boolean.
        '''
        return self._include_newlines

    @property
    def number_prompts(self):
        r'''Is true when user input getter numbers prompts.
        Otherwise false.

        Returns boolean.
        '''
        return self._number_prompts

    @property
    def prompt_character(self):
        r'''Gets user input getter prompt character.

        Returns string.
        '''
        return self._prompt_character

    @property
    def prompts(self):
        r'''Gets user input getter prompts.

        Returns list of prompts.
        '''
        return self._prompts

    @property
    def where(self):
        r'''Gets source code location strack of user input getter.

        Returns stack or none.
        '''
        return self._my_where
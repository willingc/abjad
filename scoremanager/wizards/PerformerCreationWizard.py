# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from scoremanager import iotools
from scoremanager.wizards.Wizard import Wizard


class PerformerCreationWizard(Wizard):
    r'''Performer creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_ranged',
        )

    ### INITIALIZER ###

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self._is_ranged = is_ranged

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'performer creation wizard'

    ### PRIVATE METHODS ###

    def _initialize_performer(self, performer):
        from scoremanager import wizards
        menu = self._make_performer_configuration_menu(performer)
        while True:
            result = menu._run()
            if self._should_backtrack():
                return
            elif not result:
                continue
            if result in ('skip', ['skip']):
                break
            elif result in ('more', ['more']):
                wizard = wizards.InstrumentCreationWizard(
                    session=self._session, 
                    is_ranged=True,
                    )
                instruments = wizard._run()
                if self._should_backtrack():
                    break
                if instruments is not None:
                    for instrument in instruments:
                        performer.instruments.append(instrument)
                break
            elif isinstance(result, list):
                for instrument_name in result:
                    instrument_class = \
                        instrumenttools.Instrument._default_instrument_name_to_instrument_class(
                        instrument_name)
                    instrument = instrument_class()
                    performer.instruments.append(instrument)
                break
            else:
                raise Exception("how'd we get here?")

    def _make_performer_configuration_menu(self, performer):
        menu = self._io_manager.make_menu(
            where=self._where,
            name='performer configuration',
            )
        section = menu.make_command_section(name='instrument commands')
        likely_instruments = \
            performer.likely_instruments_based_on_performer_name
        likely_instrument_names = [
            x().instrument_name for x in likely_instruments]
        likely_instrument_names.sort()
        most_likely_instrument = \
            performer.most_likely_instrument_based_on_performer_name
        default_index = None
        numbered_menu_entries = []
        if most_likely_instrument is not None:
            most_likely_instrument_name = \
                most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(
                most_likely_instrument_name)
            string = '{} (default)'.format(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = string
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            numbered_menu_entries = likely_instrument_names
            section.append(('instruments - more', 'more'))
        else:
            instrument_names = \
                instrumenttools.Instrument._list_instrument_names()
            numbered_menu_entries = instrument_names
        numbered_list_section = menu.make_numbered_list_section(
            name='select instruments',
            title='select instruments',
            default_index=default_index,
            )
        for menu_entry in numbered_menu_entries:
            numbered_list_section.append(menu_entry)
        section.append(('instruments - skip', 'skip'))
        return menu

    def _run(self, pending_user_input=None):
        from scoremanager import iotools
        if pending_user_input:
            self._session._pending_user_input = pending_user_input
        try_again = False
        performers = []
        context = iotools.ControllerContext(self)
        with context:
            while True:
                selector = \
                    iotools.Selector.make_score_tools_performer_name_selector(
                    session=self._session,
                    is_ranged=self._is_ranged,
                    )
                result = selector._run()
                if self._should_backtrack():
                    break
                if isinstance(result, list):
                    performer_names = result
                else:
                    performer_names = [result]
                performers = []
                for performer_name in performer_names:
                    performer = instrumenttools.Performer(performer_name)
                    self._initialize_performer(performer)
                    was_backtracking_locally = \
                        self._session.is_backtracking_locally
                    if self._should_backtrack():
                        if was_backtracking_locally:
                            try_again = True
                        else:
                            try_again = False
                            performers = []
                        break
                    performers.append(performer)
                if not try_again:
                    break
                else:
                    try_again = False
            if self._is_ranged and performers:
                final_result = performers[:]
            elif self._is_ranged and not performers:
                final_result = []
            elif not self._is_ranged and performers:
                final_result = performers[0]
            elif not self._is_ranged and not performers:
                final_result = None
            else:
                raise ValueError
            self._target = final_result
            return self.target
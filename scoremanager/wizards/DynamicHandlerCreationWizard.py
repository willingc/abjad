# -*- encoding: utf-8 -*-
from scoremanager.wizards.Wizard import Wizard


class DynamicHandlerCreationWizard(Wizard):
    r'''Dynamic handler creation wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_handler_editor_class_name_suffix',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager.iotools import Selector
        Wizard.__init__(
            self,
            session=session,
            target=target,
            )
        selector = Selector.make_dynamic_handler_class_name_selector(
            session=self._session,
            )
        self._selector = selector
        self._handler_editor_class_name_suffix = 'Editor'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'dynamic handler creation wizard'
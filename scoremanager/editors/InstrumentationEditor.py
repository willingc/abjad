# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import getters
from scoremanager import wizards
from scoremanager.editors.ListEditor import ListEditor


class InstrumentationEditor(ListEditor):
    r'''Instrumentation editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )
    
    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(InstrumentationEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = instrumenttools.Performer
        self._item_creator_class = wizards.PerformerCreationWizard
        self._item_creator_class_kwargs = {'is_ranged': True}
        self._item_editor_class = editors.PerformerEditor
        self._item_identifier = 'performer'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._target_name or 'instrumentation'

    ### PUBLIC PROPERTIES ###

    @property
    def _items(self):
        return self.target.performers

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            instrumenttools.InstrumentationSpecifier,
            )
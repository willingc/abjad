# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import getters
from scoremanager.editors.ListEditor import ListEditor


class TempoInventoryEditor(ListEditor):
    r'''TempoInventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        from scoremanager import iotools
        superclass = super(TempoInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = indicatortools.Tempo
        self._item_editor_class = editors.TempoEditor
        self._item_getter_configuration_method = \
            iotools.UserInputGetter.append_tempo
        self._item_identifier = 'tempo'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            indicatortools.TempoInventory,
            target_name_attribute='inventory name',
            )
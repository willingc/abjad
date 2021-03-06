# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class PatternedArticulationsHandlerEditor(Editor):
    r'''PatternedArticulationsHandler editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            handlertools.PatternedArticulationsHandler,
            ('articulation_lists', None, 'al', getters.get_lists, False),
            ('minimum_duration', None, 'nd', getters.get_duration, False),
            ('maximum_duration', None, 'xd', getters.get_duration, False),
            ('minimum_written_pitch', None, 'np', 
                getters.get_named_pitch, False),
            ('maximum_written_pitch', None, 'xp', 
                getters.get_named_pitch, False),
            )
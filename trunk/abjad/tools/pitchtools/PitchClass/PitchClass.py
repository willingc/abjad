# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class PitchClass(AbjadObject):
    '''Pitch-class base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_format_string', )

    ### INNITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PRIVATE PROPERTIES ###

    _diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
        0: 'c',
        1: 'd',
        2: 'e',
        3: 'f',
        4: 'g',
        5: 'a',
        6: 'b',
        }

    _diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
        'c': 0,
        'd': 1,
        'e': 2,
        'f': 3,
        'g': 4,
        'a': 5,
        'b': 6,
        }

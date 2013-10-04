# -*- encoding: utf-8 -*-


def pitch_class_number_to_pitch_class_name_with_flats(pitch_class_number):
    '''Change chromatic pitch-class number to chromatic pitch-class name with flats:

    ::

        >>> tmp = pitchtools.pitch_class_number_to_pitch_class_name_with_flats

    ::

        >>> for n in range(13):
        ...     pc = n / 2.0
        ...     name = tmp(pc)
        ...     print '%s   %s' % (pc, name)
        ...
        0.0   c
        0.5   dtqf
        1.0   df
        1.5   dqf
        2.0   d
        2.5   etqf
        3.0   ef
        3.5   eqf
        4.0   e
        4.5   fqf
        5.0   f
        5.5   gtqf
        6.0   gf

    Return string.
    '''

    try:
        return _pitch_class_name_to_pitch_class_number_flats[pitch_class_number]
    except KeyError:
        return _pitch_class_name_to_pitch_class_number_flats[abs(pitch_class_number)]


# TODO: externalize and make public somewhere
_pitch_class_name_to_pitch_class_number_flats = {
    0:  'c',     0.5: 'dtqf',    1: 'df',    1.5:  'dqf',
    2:  'd',     2.5: 'etqf',    3: 'ef',    3.5:  'eqf',
    4:  'e',     4.5: 'fqf',     5: 'f',     5.5:  'gtqf',
    6:  'gf',    6.5: 'gqf',     7: 'g',     7.5:  'atqf',
    8:  'af',    8.5: 'aqf',     9: 'a',     9.5:  'btqf',
    10: 'bf',   10.5: 'bqf',    11: 'b',    11.5:  'cqf',
    }
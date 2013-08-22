# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_replace_contents_of_target_container_with_contents_of_source_container_01():

    staff = Staff(Tuplet(Fraction(2, 3), "c'8 d'8 e'8") * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
        \times 2/3 {
            b'8
            c''8
            d''8 ]
        }
    }
    '''

    container = Container("c'8 d'8 e'8")
    spannertools.SlurSpanner(container.select_leaves())

    r'''
    {
        c'8 (
        d'8
        e'8 )
    }
    '''

    containertools.replace_contents_of_target_container_with_contents_of_source_container(
        staff[1], container)

    r'''
    \new Staff {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            c'8 (
            d'8
            e'8 )
        }
        \times 2/3 {
            b'8
            c''8
            d''8 ]
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
            \times 2/3 {
                c'8 (
                d'8
                e'8 )
            }
            \times 2/3 {
                b'8
                c''8
                d''8 ]
            }
        }
        '''
        )

from abjad import *


def test_beamtools_attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr_01():
    '''Beam nonnested tuplets.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr(t)

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
        }
        \times 2/3 {
            f'8 [
            g'8
            a'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t}\n\t\\times 2/3 {\n\t\tf'8 [\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_beamtools_attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr_02():
    '''Beam bottommost nested tuplets.
    '''


    inner = tuplettools.FixedDurationTuplet(Duration(2, 16), notetools.make_repeated_notes(3, Fraction(1, 16)))
    outer = tuplettools.FixedDurationTuplet(Duration(3, 16), inner * 2)
    t = Voice(outer * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            \times 2/3 {
                c'16
                d'16
                e'16
            }
            \times 2/3 {
                f'16
                g'16
                a'16
            }
        }
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            \times 2/3 {
                b'16
                c''16
                d''16
            }
            \times 2/3 {
                e''16
                f''16
                g''16
            }
        }
    }
    '''

    beamtools.attach_multiplart_beam_spanner_to_bottommost_tuplets_in_expr(t)

    r'''
    \new Voice {
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            \times 2/3 {
                c'16 [
                d'16
                e'16 ]
            }
            \times 2/3 {
                f'16 [
                g'16
                a'16 ]
            }
        }
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            \times 2/3 {
                b'16 [
                c''16
                d''16 ]
            }
            \times 2/3 {
                e''16 [
                f''16
                g''16 ]
            }
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t\\tweak #'text #tuplet-number::calc-fraction-text\n\t\\times 3/4 {\n\t\t\\times 2/3 {\n\t\t\tc'16 [\n\t\t\td'16\n\t\t\te'16 ]\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tf'16 [\n\t\t\tg'16\n\t\t\ta'16 ]\n\t\t}\n\t}\n\t\\tweak #'text #tuplet-number::calc-fraction-text\n\t\\times 3/4 {\n\t\t\\times 2/3 {\n\t\t\tb'16 [\n\t\t\tc''16\n\t\t\td''16 ]\n\t\t}\n\t\t\\times 2/3 {\n\t\t\te''16 [\n\t\t\tf''16\n\t\t\tg''16 ]\n\t\t}\n\t}\n}"
from abjad import *


def test_beamtools_attach_beam_spanners_to_measures_in_expr_01():
    '''Beam all measures in expr with plain old Beam spanner.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
    }
    '''

    beamtools.attach_beam_spanners_to_measures_in_expr(staff)


    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"
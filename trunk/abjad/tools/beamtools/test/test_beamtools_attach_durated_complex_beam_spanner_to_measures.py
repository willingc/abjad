from abjad import *


def test_beamtools_attach_durated_complex_beam_spanner_to_measures_01():
    '''Apply DuratedComplexBeam to all measures in measures;
    set p.durations equal to preprolated measure durations.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

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

    measures = staff[:]
    beamtools.attach_durated_complex_beam_spanner_to_measures(measures)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            d'8
        }
        {
            \time 2/8
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            e'8
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            f'8 ]
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #1\n\t\tc'8 [\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #1\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #1\n\t\te'8\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #0\n\t\tf'8 ]\n\t}\n}"
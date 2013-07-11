from abjad.tools import spannertools


def attach_durated_complex_beam_spanner_to_measures(measures):
    r'''.. versionadded:: 1.1

    Apply durated complex beam spanner to `measures`::

        >>> staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> measures = staff[:]
        >>> beamtools.attach_durated_complex_beam_spanner_to_measures(measures)
        DuratedComplexBeamSpanner(|2/8(2)|, |2/8(2)|)

    ::

        >>> f(staff)
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
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #1
                e'8
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #0
                f'8 ]
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Set beam spanner durations to preprolated measure durations.

    Return beam spanner created.
    '''
    from abjad.tools import beamtools

    # collect measures
    durations = []
    for measure in measures:
        spannertools.detach_spanners_attached_to_component(
            measure,
            spanner_classes=(beamtools.BeamSpanner,)
            )
        durations.append(measure.preprolated_duration)

    # beam measures
    beam = beamtools.DuratedComplexBeamSpanner(
        measures,
        durations=durations,
        span=1,
        )

    # return beam
    return beam
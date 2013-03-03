def replace_components_with_children_of_components(components):
    r'''.. versionadded:: 1.1

    Remove arbitrary `components` from score but retain children of `components` in score::

        >>> staff = Staff(Container(notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
        >>> spannertools.SlurSpanner(staff[:])
        SlurSpanner({c'8, d'8}, {e'8, f'8})
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                c'8 [ (
                d'8
            }
            {
                e'8
                f'8 ] )
            }
        }

    ::

        >>> componenttools.replace_components_with_children_of_components(staff[0:1])
        Selection({},)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ (
            d'8
            {
                e'8
                f'8 ] )
            }
        }

    Return `components`.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_components(components)

    for component in components:
        parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
        # to avoid slice assigment errors in pychecker
        #result = parent[start:stop+1] = list(getattr(component, 'music', ()))
        music_list = list(getattr(component, 'music', ()))
        parent.__setitem__(slice(start, stop + 1), music_list)
    return components

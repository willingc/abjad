# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_logical_voice_from_component(
    component, 
    component_class=None, 
    reverse=False,
    ):
    r'''Itearte thread forward from `component` and yield instances 
    of `component_class`.

    ::

        >>> container = Container(Voice(notetools.make_repeated_notes(2)) * 2)
        >>> container.is_simultaneous = True
        >>> container[0].name = 'voice 1'
        >>> container[1].name = 'voice 2'
        >>> staff = Staff(container * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
            <<
                \context Voice = "voice 1" {
                    g'8
                    a'8
                }
                \context Voice = "voice 2" {
                    b'8
                    c''8
                }
            >>
        }

    Starting from the first leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[0], Note):
        ...     x
        ...
        Note("c'8")
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Starting from the second leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[1], Note):
        ...     x
        ...
        Note("d'8")
        Note("g'8")
        Note("a'8")

    Yield all components in thread:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[0]):
        ...     x
        ...
        Note("c'8")
        Voice-"voice 1"{2}
        Note("d'8")
        Voice-"voice 1"{2}
        Note("g'8")
        Note("a'8")

    Iterate thread backward from `component` and yield instances 
    of `component_class`, starting from the last leaf in score:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[-1], 
        ...     Note, 
        ...     reverse=True,
        ...     ):
        ...     x
        Note("c''8")
        Note("b'8")
        Note("f'8")
        Note("e'8")

    Yield all components in thread:

    ::

        >>> for x in iterationtools.iterate_logical_voice_from_component(
        ...     staff.select_leaves(allow_discontiguous_leaves=True)[-1], 
        ...     reverse=True,
        ...     ):
        ...     x
        Note("c''8")
        Voice-"voice 2"{2}
        Note("b'8")
        Voice-"voice 2"{2}
        Note("f'8")
        Note("e'8")

    Return generator.
    '''
    from abjad.tools import iterationtools

    # set default class
    if component_class is None:
        component_class = componenttools.Component

    # save thread signature of input component
    component_thread_signature = \
        component._select_parentage().containment_signature

    # iterate component depth-first allowing to crawl UP into score
    if not reverse:
        for x in iterationtools.iterate_components_depth_first(component, capped=False):
            if isinstance(x, component_class):
                if x._select_parentage().containment_signature == \
                    component_thread_signature:
                    yield x
    else:
        for x in iterationtools.iterate_components_depth_first(component, capped=False, direction=Right):
            if isinstance(x, component_class):
                if x._select_parentage().containment_signature == \
                    component_thread_signature:
                    yield x
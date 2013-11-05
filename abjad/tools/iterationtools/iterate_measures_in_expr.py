# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


def iterate_measures_in_expr(expr, reverse=False, start=0, stop=None):
    r'''Iterate measures forward in `expr`:

    ::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")

    ..  doctest::

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
            {
                g'8
                a'8
            }
        }

    ::

        >>> for measure in iterationtools.iterate_measures_in_expr(staff):
        ...     measure
        ...
        Measure(2/8, [c'8, d'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [g'8, a'8])

    Use the optional `start` and `stop` keyword parameters to control
    the start and stop indices of iteration. ::

        >>> for measure in iterationtools.iterate_measures_in_expr(
        ...     staff, start=1):
        ...     measure
        ...
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [g'8, a'8])

    ::

        >>> for measure in iterationtools.iterate_measures_in_expr(
        ...     staff, start=0, stop=2):
        ...     measure
        ...
        Measure(2/8, [c'8, d'8])
        Measure(2/8, [e'8, f'8])

    Iterate measures backward in `expr`:

    ::

        >>> for measure in iterationtools.iterate_measures_in_expr(
        ...     staff, reverse=True):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    Use the optional `start` and `stop` keyword parameters
    to control indices of iteration. ::

        >>> for measure in iterationtools.iterate_measures_in_expr(
        ...     staff, start=1, reverse=True):
        ...     measure
        ...
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    ::

        >>> for measure in iterationtools.iterate_measures_in_expr(
        ...     staff, start=0, stop=2, reverse=True):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])

    Iterates across different logical voices.

    Returns generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr,
        component_class=scoretools.Measure,
        reverse=reverse,
        start=start,
        stop=stop,
        )
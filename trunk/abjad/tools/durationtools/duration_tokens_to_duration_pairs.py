def duration_tokens_to_duration_pairs(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to duration pairs::

        >>> durationtools.duration_tokens_to_duration_pairs([Fraction(2, 4), 3, '8.', (5, 16)])
        [(1, 2), (3, 1), (3, 16), (5, 16)]

    Return new object of `duration_tokens` type.
    '''
    from abjad.tools import durationtools

    return type(duration_tokens)([
        durationtools.Duration(x).pair for x in duration_tokens])

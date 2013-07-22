from abjad.tools import pitchtools


def analyze_incomplete_chord(expr):
    '''.. versionadded:: 2.0

    Analyze `expr` and return chord class based on incomplete pitches. ::

        >>> tonalanalysistools.analyze_incomplete_chord(Chord([7, 11], (1, 4)))
        GMajorTriadInRootPosition

    ::

        >>> tonalanalysistools.analyze_incomplete_chord(Chord(['fs', 'g', 'b'], (1, 4)))
        GMajorSeventhInSecondInversion

    Return chord class.
    '''
    from abjad.tools import tonalanalysistools

    #print 'expr is %s ...' % str(expr)

    pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
    npcset = pitchtools.NamedChromaticPitchClassSet(pitches)
    dicv = npcset.inversion_equivalent_diatonic_interval_class_vector

    #print npcset
    #print dicv

    # TODO: eliminate code duplication #

    if dicv == _make_dicv('c', 'ef'):
        model_npcs = ['c', 'ef']
        quality, extent = 'minor', 'triad'

    elif dicv == _make_dicv('c', 'e'):
        model_npcs = ['c', 'e']
        quality, extent = 'major', 'triad'

    elif dicv == _make_dicv('c', 'ef', 'bff'):
        model_npcs = ['c', 'ef', 'bff']
        quality, extent = 'diminished', 'seventh'

    elif dicv == _make_dicv('c', 'ef', 'bf'):
        model_npcs = ['c', 'ef', 'bf']
        quality, extent = 'minor', 'seventh'

    elif dicv == _make_dicv('c', 'e', 'bf'):
        model_npcs = ['c', 'e', 'bf']
        quality, extent = 'dominant', 'seventh'

    elif dicv == _make_dicv('c', 'e', 'b'):
        model_npcs = ['c', 'e', 'b']
        quality, extent = 'major', 'seventh'

    else:
        raise TonalHarmonyError('can not identify incomplete tertian chord.')

    #print 'model npcs are %s ...' % model_npcs

    bass = min(pitches).named_chromatic_pitch_class

    try:
        npcseg = npcset.order_by(pitchtools.NamedChromaticPitchClassSegment(model_npcs))
    except ValueError:
        raise TonalHarmonyError('can not identify incomplete tertian chord.')

    inversion = npcseg.index(bass)
    root = npcseg[0]

    return tonalanalysistools.ChordClass(root, quality, extent, inversion)


def _make_dicv(*named_chromatic_pitch_classes):
    npcset = pitchtools.NamedChromaticPitchClassSet(named_chromatic_pitch_classes)
    return npcset.inversion_equivalent_diatonic_interval_class_vector
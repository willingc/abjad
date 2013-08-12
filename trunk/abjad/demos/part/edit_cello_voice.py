# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import chordtools
from abjad.tools import marktools
from abjad.tools import notetools
from abjad.tools.selectiontools import more


def edit_cello_voice(score, durated_reservoir):

    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']

    tie_chain = more(voice[-1]).select_tie_chain()
    for leaf in tie_chain.leaves:
        parent = leaf._select_parentage().parent
        index = parent.index(leaf)
        parent[index] = chordtools.Chord(['e,', 'a,'], leaf.written_duration)

    unison_descent = voice[-len(descents[-1]):].copy_and_detach_spanners()
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = more(chord).select_parentage().parent.index(chord)
        parent[index] = notetools.Note(
            chord.written_pitches[1], chord.written_duration)
        marktools.Articulation('accent')(parent[index])
        marktools.Articulation('tenuto')(parent[index])

    voice.extend('a,1. ~ a,2 b,1 ~ b,1. ~ b,1. a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2 r4 r2.')

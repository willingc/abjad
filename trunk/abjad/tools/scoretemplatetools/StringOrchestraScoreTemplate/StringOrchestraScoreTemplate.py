# -*- encoding: utf-8 -*-
import collections
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StringOrchestraScoreTemplate(AbjadObject):
    '''String orchestra score template.

    ::

        >>> template = scoretemplatetools.StringOrchestraScoreTemplate(
        ...     violin_count=6,
        ...     viola_count=4,
        ...     cello_count=3,
        ...     contrabass_count=2,
        ...     )
        >>> score = template()

    ::

        >>> score
        Score-"String Orchestra Score"<<4>>

    ..  doctest::
                
        >>> f(score)        
        \context Score = "String Orchestra Score" <<
            \context StaffGroup = "Violin Staff Group" <<
                \context Staff = "Violin 1 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 1 Voice" {
                    }
                }
                \context Staff = "Violin 2 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 2 Voice" {
                    }
                }
                \context Staff = "Violin 3 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 3 Voice" {
                    }
                }
                \context Staff = "Violin 4 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 4 Voice" {
                    }
                }
                \context Staff = "Violin 5 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 5 Voice" {
                    }
                }
                \context Staff = "Violin 6 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Violin 6 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Viola Staff Group" <<
                \context Staff = "Viola 1 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola 1 Voice" {
                    }
                }
                \context Staff = "Viola 2 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola 2 Voice" {
                    }
                }
                \context Staff = "Viola 3 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola 3 Voice" {
                    }
                }
                \context Staff = "Viola 4 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola 4 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Cello Staff Group" <<
                \context Staff = "Cello 1 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello }
                    \set Staff.shortInstrumentName = \markup { Vc. }
                    \context Voice = "Cello 1 Voice" {
                    }
                }
                \context Staff = "Cello 2 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello }
                    \set Staff.shortInstrumentName = \markup { Vc. }
                    \context Voice = "Cello 2 Voice" {
                    }
                }
                \context Staff = "Cello 3 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello }
                    \set Staff.shortInstrumentName = \markup { Vc. }
                    \context Voice = "Cello 3 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Contrabass Staff Group" <<
                \context Staff = "Contrabass 1 Voice" {
                    \clef "bass_8"
                    \set Staff.instrumentName = \markup { Contrabass }
                    \set Staff.shortInstrumentName = \markup { Vb. }
                    \context Voice = "Contrabass 1 Voice" {
                    }
                }
                \context Staff = "Contrabass 2 Voice" {
                    \clef "bass_8"
                    \set Staff.instrumentName = \markup { Contrabass }
                    \set Staff.shortInstrumentName = \markup { Vb. }
                    \context Voice = "Contrabass 2 Voice" {
                    }
                }
            >>
        >>

    Return score template.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        violin_count=6,
        viola_count=4,
        cello_count=3,
        contrabass_count=2,
        ):
        assert 0 <= violin_count
        assert 0 <= viola_count
        assert 0 <= cello_count
        assert 0 <= contrabass_count
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)

    ### SPECIAL METHODS ###

    def __call__(self):

        string_orchestra_score = scoretools.Score(
            name='String Orchestra Score',
            )

        if self.violin_count:
            violin_staff_group = scoretools.StaffGroup(
                name='Violin Staff Group',
                )
            for i in range(1, self.violin_count + 1):
                violin_voice = voicetools.Voice(
                    name='Violin {} Voice'.format(i),
                    )
                violin_staff = stafftools.Staff(
                    [violin_voice], name='Violin {} Voice'.format(i))
                contexttools.ClefMark('treble').attach(violin_staff)
                instrumenttools.Violin().attach(violin_staff)
                violin_staff_group.append(violin_staff)
            string_orchestra_score.append(violin_staff_group)

        if self.viola_count:
            viola_staff_group = scoretools.StaffGroup(
                name='Viola Staff Group',
                )
            for i in range(1, self.viola_count + 1):
                viola_voice = voicetools.Voice(
                    name='Viola {} Voice'.format(i),
                    )
                viola_staff = stafftools.Staff(
                    [viola_voice], name='Viola {} Voice'.format(i))
                contexttools.ClefMark('alto').attach(viola_staff)
                instrumenttools.Viola().attach(viola_staff)
                viola_staff_group.append(viola_staff)
            string_orchestra_score.append(viola_staff_group)

        if self.cello_count:
            cello_staff_group = scoretools.StaffGroup(
                name='Cello Staff Group',
                )
            for i in range(1, self.cello_count + 1):
                cello_voice = voicetools.Voice(
                    name='Cello {} Voice'.format(i),
                    )
                cello_staff = stafftools.Staff(
                    [cello_voice], name='Cello {} Voice'.format(i))
                contexttools.ClefMark('bass').attach(cello_staff)
                instrumenttools.Cello().attach(cello_staff)
                cello_staff_group.append(cello_staff)
            string_orchestra_score.append(cello_staff_group)

        if self.contrabass_count:
            contrabass_staff_group = scoretools.StaffGroup(
                name='Contrabass Staff Group',
                )
            for i in range(1, self.contrabass_count + 1):
                contrabass_voice = voicetools.Voice(
                    name='Contrabass {} Voice'.format(i),
                    )
                contrabass_staff = stafftools.Staff(
                    [contrabass_voice], name='Contrabass {} Voice'.format(i))
                contexttools.ClefMark('bass_8').attach(contrabass_staff)
                instrumenttools.Contrabass().attach(contrabass_staff)
                contrabass_staff_group.append(contrabass_staff)
            string_orchestra_score.append(contrabass_staff_group)

        # return string quartet score
        return string_orchestra_score

    ### PUBLIC PROPERTIES ###

    @property
    def contrabass_count(self):
        return self._contrabass_count

    @property
    def cello_count(self):
        return self._cello_count

    @property
    def viola_count(self):
        return self._viola_count

    @property
    def violin_count(self):
        return self._violin_count
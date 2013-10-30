from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class WindungenScoreTemplate(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        assert 0 < staff_count
        self.staff_count = int(staff_count)

    ### SPECIAL METHODS ###

    def __call__(self):
        staves = []
        for index in range(self.staff_count):
            number = index + 1
            voice = scoretools.Voice(name='Voice {}'.format(number))
            staff = scoretools.Staff([voice], name='Staff {}'.format(number))
            clef = contexttools.ClefMark('bass')
            attach(clef, staff)
            cello = instrumenttools.Cello(
                instrument_name='Cello {}'.format(number),
                short_instrument_name='Vc. {}'.format(number),
                )
            attach(cello, staff)
            staff.override.stem.stemlet_length = 2
            staff.override.beam.damping = '+inf.0'
            staves.append(staff)

        windungen_staff_group = scoretools.StaffGroup(
            staves, 
            name='Windungen Staff Group',
            )

        windungen_score = scoretools.Score(
            [windungen_staff_group], 
            name='Windungen Score',
            )

        return windungen_score

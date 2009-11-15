from abjad import *


def test_iterate_measures_forward_in_01( ):

   staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(staff)

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
           {
                   \time 2/8
                   g'8
                   a'8
           }
   }
   '''

   measures = list(iterate.measures_forward_in(staff))
   
   assert measures[0] is staff[0]
   assert measures[1] is staff[1]
   assert measures[2] is staff[2]


def test_iterate_measures_forward_in_02( ):
   '''Optional start and stop keyword paramters.'''

   staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(staff)

   measures = list(iterate.measures_forward_in(staff, start = 1))
   assert measures[0] is staff[1]
   assert measures[1] is staff[2]
   assert len(measures) == 2

   measures = list(iterate.measures_forward_in(staff, stop = 2))
   assert measures[0] is staff[0]
   assert measures[1] is staff[1]
   assert len(measures) == 2

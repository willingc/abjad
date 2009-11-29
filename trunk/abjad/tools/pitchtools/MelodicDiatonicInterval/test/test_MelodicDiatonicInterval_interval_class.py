from abjad import *


def test_MelodicDiatonicInterval_interval_class_01( ):

   diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 1)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', 2)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 3)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', 3)
   assert diatonic_interval.interval_class == 3


def test_MelodicDiatonicInterval_interval_class_02( ):

   diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', 8)
   assert diatonic_interval.interval_class == 1

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', 9)
   assert diatonic_interval.interval_class == 2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 10)
   assert diatonic_interval.interval_class == 3

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', 10)
   assert diatonic_interval.interval_class == 3


def test_MelodicDiatonicInterval_interval_class_03( ):

   diatonic_interval = pitchtools.MelodicDiatonicInterval('perfect', -8)
   assert diatonic_interval.interval_class == -1

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', -9)
   assert diatonic_interval.interval_class == -2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', -9)
   assert diatonic_interval.interval_class == -2

   diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', -10)
   assert diatonic_interval.interval_class == -3

   diatonic_interval = pitchtools.MelodicDiatonicInterval('major', -10)
   assert diatonic_interval.interval_class == -3

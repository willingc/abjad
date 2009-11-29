from abjad.tools import mathtools
from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval


class _ChromaticInterval(_Interval):
   '''.. versionaddedd:: 1.1.2

   Abstract chromatic interval class from which concrete classes inherit.
   '''

   def __init__(self, arg):
      if isinstance(arg, (int, float, long)):
         self._interval_number = arg
      elif isinstance(arg, _Interval):
         self._interval_number = arg.semitones
      else:
         raise TypeError('%s must be number or interval.' % arg)

   ## OVERLOADS ##

   def __abs__(self):
      from abjad.tools.pitchtools.HarmonicChromaticInterval import \
         HarmonicChromaticInterval
      return HarmonicChromaticInterval(abs(self._interval_number))

   def __add__(self, arg):
      if isinstance(arg, self.__class__):
         interval_number = self.interval_number + arg.interval_number
         return self.__class__(interval_number)
      raise TypeError('must be %s.'% self.__class__)

   def __copy__(self):
      return self.__class__(self.interval_number)

   def __eq__(self, arg):
      if isinstance(arg, self.__class__):
         if self.interval_number == arg.interval_number:
            return True
      return False

   def __float__(self):
      return float(self._interval_number)

   def __int__(self):
      return int(self._interval_number)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._interval_number)

   def __sub__(self, arg):
      if isinstance(arg, self.__class__):
         interval_number = self.interval_number - arg.interval_number
         return self.__class__(interval_number)
      raise TypeError('must be %s' % self.__class__)

   ## PUBLIC ATTRIBUTES ##

   @property
   def semitones(self):
      return self.interval_number

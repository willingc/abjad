class _IntervalClassSegment(list):
   '''.. versionadded:: 1.1.2

   Abstract ordered colleciton of interval class instances
   from which concrete classes inherit.
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_numbers(self):
      return tuple([interval_class.number for interval_class in self])

   @property
   def interval_classes(self):
      return tuple(self[:])

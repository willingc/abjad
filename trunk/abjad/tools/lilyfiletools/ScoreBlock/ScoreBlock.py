from abjad.tools.lilyfiletools._BlockNonattributed import _BlockNonattributed


class ScoreBlock(_BlockNonattributed):
   r'''.. versionadded:: 1.1.2

   Abjad model of LilyPond input file score block.
   '''

   def __init__(self):
      _BlockNonattributed.__init__(self)
      self._escaped_name = r'\score'

from abjad.accidental.interface import _AccidentalInterface
from abjad.articulations.interface import _ArticulationsInterface
from abjad.barline.interface import _BarLineInterface
from abjad.barnumber.interface import _BarNumberInterface
from abjad.beam.interface import _BeamInterface
from abjad.breaks.interface import _BreaksInterface
from abjad.comments.comments import _UserComments
from abjad.core.abjadcore import _Abjad
from abjad.clef.interface import _ClefInterface
from abjad.directives.interface import _UserDirectivesInterface
from abjad.dots.interface import _DotsInterface
from abjad.dynamics.interface import _DynamicsInterface
from abjad.glissando.interface import _GlissandoInterface
from abjad.instrument.interface import _InstrumentInterface
from abjad.interfaces.aggregator import _InterfaceAggregator
from abjad.meter.interface import _MeterInterface
from abjad.navigator.navigator import _Navigator
from abjad.notecolumn.interface import _NoteColumnInterface
#from abjad.notehead.interface import _NoteHeadInterface
from abjad.numbering.interface import _NumberingInterface
from abjad.offset.interface import _OffsetInterface
from abjad.parentage.parentage import _Parentage
from abjad.pianopedal.interface import _PianoPedalInterface
from abjad.rational import Rational
from abjad.receipt.component import _ComponentReceipt
#from abjad.rest.interface import _RestInterface
#from abjad.score.interface.interface import _ScoreInterface
from abjad.slur.interface import _SlurInterface
from abjad.spacing.interface import _SpacingInterface
from abjad.spanbar.interface import _SpanBarInterface
#from abjad.staff.interface.interface import _StaffInterface
from abjad.stem.interface import _StemInterface
from abjad.tempo.interface import _TempoInterface
from abjad.thread.interface import _ThreadInterface
from abjad.tie.interface import _TieInterface
from abjad.text.interface import _TextInterface
from abjad.tremolo.interface import _TremoloInterface
from abjad.trill.interface import _TrillInterface
#from abjad.tuplet.bracket import _TupletBracketInterface
#from abjad.tuplet.number import _TupletNumberInterface
from abjad.update.interface import _UpdateInterface
#from abjad.voice.interface.interface import _VoiceInterface
import copy
import types


class _Component(_Abjad):

   def __init__(self):
      '''Late import of _RestInterface, _ScoreInterface, _StaffInterface
      and _VoiceInterface to avoid circular imports in which instantiating
      a rest imports abjad/leaf (because Rest is a _Leaf), which imports 
      abjad/component (because _Leaf is a _Component), which imports 
      abjad/rest (because _Component has a _RestInterface).
   
      The solution given here with the late imports of what we might
      collectively term the 'component information interfaces' does indeed
      work but also suggests a cleaner way of laying out the codebase
      in which ALL interfaces of whatever sort, not just the component
      information interfaces imported here, collectively live inside
      some abjad/allinterfaces package.'''
      from abjad.notehead.interface import _NoteHeadInterface
      from abjad.rest.interface import _RestInterface
      from abjad.score.interface.interface import _ScoreInterface
      from abjad.staff.interface.interface import _StaffInterface
      from abjad.tuplet.bracket import _TupletBracketInterface
      from abjad.tuplet.number import _TupletNumberInterface
      from abjad.voice.interface.interface import _VoiceInterface
      self._interfaces = _InterfaceAggregator(self)
      self._accidental = _AccidentalInterface(self)
      self._articulations = _ArticulationsInterface(self)
      self._barline = _BarLineInterface(self)
      self._barnumber = _BarNumberInterface(self)
      self._beam = _BeamInterface(self)
      self._breaks = _BreaksInterface(self)
      self._comments = _UserComments( )
      self._directives = _UserDirectivesInterface(self)
      self._dots = _DotsInterface(self)
      self._dynamics = _DynamicsInterface(self)
      self._glissando = _GlissandoInterface(self)
      self._history = { }
      self._instrument = _InstrumentInterface(self)
      self._name = None
      self._navigator = _Navigator(self)
      self._notecolumn = _NoteColumnInterface(self)
      self._notehead = _NoteHeadInterface(self)
      self._parentage = _Parentage(self)
      self._pianopedal = _PianoPedalInterface(self)
      self._rest = _RestInterface(self)
      self._score = _ScoreInterface(self)
      self._slur = _SlurInterface(self)
      self._spacing = _SpacingInterface(self)
      self._spanbar = _SpanBarInterface(self)
      self._stem = _StemInterface(self)
      self._text = _TextInterface(self)
      self._thread = _ThreadInterface(self)
      self._tie = _TieInterface(self)
      self._tremolo = _TremoloInterface(self)
      self._trill = _TrillInterface(self)
      self._tupletbracket = _TupletBracketInterface(self)
      self._tupletnumber = _TupletNumberInterface(self)
      self._update = _UpdateInterface(self)
      ## Observer interfaces must instantiate lexically after _UpdateInterface
      self._clef = _ClefInterface(self, self._update)
      self._meter = _MeterInterface(self, self._update)
      self._numbering = _NumberingInterface(self, self._update)
      self._offset = _OffsetInterface(self, self._update)
      self._staff = _StaffInterface(self, self._update)
      self._tempo = _TempoInterface(self, self._update)
      self._voice = _VoiceInterface(self)

   ## OVERLOADS ##

   def __mul__(self, n):
      from abjad.tools import clone
      return clone.unspan([self], n)

   def __rmul__(self, n):
      return self * n

   ## PRIVATE ATTRIBUTES ##

   @property
   def _ID(self):
      if self.name is not None:
         rhs = self.name
      else:
         rhs = id(self)
      lhs = self.__class__.__name__
      return '%s-%s' % (lhs, rhs)

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      return self._accidental

   @property
   def articulations(self):
      return self._articulations
   
   @property
   def barline(self):
      return self._barline

   @property
   def barnumber(self):
      return self._barnumber
   
   @property
   def beam(self):
      return self._beam

   @property
   def breaks(self):
      return self._breaks

   @property
   def clef(self):
      return self._clef

   @property
   def comments(self):
      return self._comments

   @property
   def directives(self):
      return self._directives

   @property
   def dots(self):
      return self._dots

   @property
   def duration(self):
      return self._duration

   @property
   def dynamics(self):
      return self._dynamics

   @property
   def format(self):
      return self.formatter.format

   @property
   def formatter(self):
      return self._formatter

   @property
   def glissando(self):
      return self._glissando

   @property
   def history(self):
      return self._history

   @property
   def instrument(self):
      return self._instrument

   @property
   def interfaces(self):
      return self._interfaces

   @property
   def leaves(self):
      '''Python list of all leaves in container.'''
      from abjad.leaf.leaf import _Leaf
      from abjad.tools import iterate
      return list(iterate.naive(self, _Leaf))

   @property
   def meter(self):
      return self._meter

   @property
   def music(self):
      if hasattr(self, '_music'):
         return tuple(self._music)
      else:
         return tuple( )

   @apply
   def name( ):
      def fget(self):
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._name = arg
      return property(**locals( ))

   @property
   def notecolumn(self):
      return self._notecolumn

   @property
   def notehead(self):
      return self._notehead

#   @property
#   def numbering(self):
#      return self._numbering

   @property
   def offset(self):
      return self._offset

   @property
   def parentage(self):
      return self._parentage

   @property
   def pianopedal(self):
      return self._pianopedal

   @property
   def rest(self):
      return self._rest

   @property
   def score(self):
      return self._score

   @property
   def slur(self):
      return self._slur

   @property
   def spacing(self):
      return self._spacing

   @property
   def spanbar(self):
      return self._spanbar

   @property
   def spanners(self):
      return self._spanners
   
   @property
   def staff(self):
      return self._staff

   @property
   def stem(self):
      return self._stem

   @property
   def thread(self):
      return self._thread

   @property
   def tie(self):
      return self._tie

   @property
   def tempo(self):
      return self._tempo

   @property
   def text(self):
      return self._text

   @property
   def tremolo(self):
      return self._tremolo

   @property
   def trill(self):
      return self._trill
   
   @property
   def tupletbracket(self):
      return self._tupletbracket

   @property
   def tupletnumber(self):
      return self._tupletnumber

   @property
   def voice(self):
      return self._voice

   ## PUBLIC METHODS ##

   def extend_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` rightwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(construct.scale(3))
         abjad> Beam(t[:])
         abjad> t[-1].extend_in_parent(construct.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
         }
      '''

      from abjad.tools import check
      from abjad.tools import parenttools
      check.assert_components(components)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         after = stop + 1
         parent[after:after] = components
      return [self] + components

   def extend_left_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` leftwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(construct.scale(3))
         abjad> Beam(t[:])
         abjad> t[0].extend_in_parent(construct.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 
            d'8
            e'8 
            c'8 [
            d'8
            e'8 ]
         }
      '''

      from abjad.tools import check
      from abjad.tools import parenttools
      check.assert_components(components)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         parent[start:start] = components
      return components + [self] 

   def splice(self, components):
      '''Splice `components` after `self`.
      Extend spanners rightwards to attach to all components in list.'''
      from abjad.tools import check
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      check.assert_components(components)
      insert_offset = self.offset.prolated.stop
      receipt = spannertools.get_dominant([self])
      for spanner, index in receipt:
         insert_component = spannertools.find_component_at_score_offset(
            spanner, insert_offset)
         if insert_component is not None:
            insert_index = spanner.index(insert_component)
         else:
            insert_index = len(spanner)
         for component in reversed(components):
            spanner._insert(insert_index, component)
            component.spanners._add(spanner)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start + 1, component)
      return [self] + components

   def splice_left(self, components):
      '''Splice `components` before `self`.
      Extend spanners leftwards to attach to all components in list.'''
      from abjad.tools import check
      from abjad.tools import parenttools
      from abjad.tools import spannertools
      check.assert_components(components)
      offset = self.offset.prolated.start
      receipt = spannertools.get_dominant([self])
      for spanner, x in receipt:
         index = spannertools.find_index_at_score_offset(spanner, offset)
         for component in reversed(components):
            spanner._insert(index, component)
            component.spanners._add(spanner)
      parent, start, stop = parenttools.get_with_indices([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start, component)
      return components + [self] 

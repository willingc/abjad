from abjad.tools import contexttools
from abjad.tools import durtools
from abjad.tools.componenttools.clone_components_and_fracture_crossing_spanners import clone_components_and_fracture_crossing_spanners
from abjad.tools.metertools import Meter


def clone_components_and_immediate_parent_of_first_component(components):
   r'''.. versionadded:: 1.1.1

   Clone `components` and immediate parent of first component.

   The `components` must be thread-contiguous.
   
   Return in newly created container equal to type of 
   first element in `copmonents`.

   If the parent of the first element in `components` is a tuplet then
   insure that the tuplet multiplier of the function output
   equals the tuplet multiplier of the parent of the 
   first element in `components`. ::

      abjad> voice = Voice(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 3)
      abjad> macros.diatonicize(voice)
      abjad> beam = spannertools.BeamSpanner(voice.leaves[:4])
      abjad> f(voice)
      \new Voice {
              \times 2/3 {
                      c'8 [
                      d'8
                      e'8
              }
              \times 2/3 {
                      f'8 ]
                      g'8
                      a'8
              }
              \times 2/3 {
                      b'8
                      c''8
                      d''8
              }
      }
      abjad> new_tuplet = componenttools.clone_components_and_immediate_parent_of_first_component(voice.leaves[:2])
      abjad> new_tuplet
      FixedDurationTuplet(1/6, [c'8, d'8])
      abjad> f(new_tuplet)
      \times 2/3 {
              c'8 [
              d'8 ]
      }   

   Parent-contiguity is not required.
   Thread-contiguous `components` suffice. ::
   
      abjad> new_tuplet = componenttools.clone_components_and_immediate_parent_of_first_component(voice.leaves[:5])
      abjad> new_tuplet
      FixedDurationTuplet(5/12, [c'8, d'8, e'8, f'8, g'8])
      abjad> f(new_tuplet)
      \times 2/3 {
              c'8 [
              d'8
              e'8
              f'8 ]
              g'8
      }

   .. note:: this function copies only the *immediate parent* of
      the first element in `components`. This function ignores any further 
      parentage of `components` above the immediate parent of `components`.

   .. todo:: this function should (but does not) copy marks that attach to `components` and
      to the immediate parent of the first component; extend function to do so.

   .. versionchanged:: 1.1.2
      renamed ``clonewp.with_parent( )`` to
      ``componenttools.clone_components_and_immediate_parent_of_first_component( )``.
   '''
   from abjad.tools import componenttools
   from abjad.tools.measuretools.Measure import Measure

   # assert strictly contiguous components in same thread
   assert componenttools.all_are_thread_contiguous_components(components)

   # remember parent
   parent = components[0]._parentage.parent

   # new: remember parent multiplier, if any
   parent_multiplier = getattr(parent.duration, 'multiplier', 1)

   # new: remember parent denominator, if any
   if isinstance(parent, Measure):
      parent_denominator = contexttools.get_effective_time_signature(parent).denominator
   else:
      parent_denominator = None

   # remember parent's music
   parents_music = components[0]._parentage.parent._music

   # strip parent of music temporarily
   parent._music = [ ]

   # copy parent without music
   result = clone_components_and_fracture_crossing_spanners([parent])[0]

   # give music back to parent
   parent._music = parents_music

   # populate result with references to input list
   result._music.extend(components)

   # populate result with deepcopy of input list and fracture spanners
   result = clone_components_and_fracture_crossing_spanners([result])[0]

   # point elements in result to result as new parent
   for element in result:
      element._parentage._switch(result)

   ## TODO: change hard-coded class name testing to isinstance testing instead
   # new: resize result to match parent_multiplier, if resizable
   if result.__class__.__name__ == 'FixedDurationTuplet':
      result.duration.target = parent_multiplier * result.duration.contents
   elif result.__class__.__name__ == 'Measure':
      new_duration = parent_multiplier * result.duration.contents
      result._attach_explicit_meter(new_duration.numerator, new_duration.denominator)

   # new: rewrite result denominator, if available
   if parent_denominator is not None:
      old_meter = contexttools.get_effective_time_signature(result)
      old_meter_pair = (old_meter.numerator, old_meter.denominator)
      new_meter = durtools.rational_to_duration_pair_with_specified_integer_denominator(
         old_meter_pair, parent_denominator)
      result._attach_explicit_meter(*new_meter)

   # return copy
   return result

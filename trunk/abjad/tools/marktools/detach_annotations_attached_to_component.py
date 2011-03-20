from abjad.tools.marktools.get_annotations_attached_to_component import get_annotations_attached_to_component


def detach_annotations_attached_to_component(component):
   r'''.. versionadded:: 1.1.2
   
   Detach annotations attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> marktools.Annotation('annotation 1')(staff[0])
      abjad> marktools.Annotation('annotation 2')(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         c'8 (
         d'8
         e'8
         f'8 )
      }


   ::

      abjad> marktools.get_annotations_attached_to_component(staff[0])
      (Annotation('annotation 1')(c'8), Annotation('annotation 2')(c'8))

   ::

      abjad> marktools.detach_annotations_attached_to_component(staff[0])
      (Annotation('annotation 1')(c'8), Annotation('annotation 2')(c'8))

   ::

      abjad> marktools.get_annotations_attached_to_components(staff[0])
      ()
      
   Return tuple or zero or more annotations detached.
   '''

   annotations = [ ]
   for annotation in get_annotations_attached_to_component(component):
      annotation.detach_mark( )
      annotations.append(annotation)

   return tuple(annotations)

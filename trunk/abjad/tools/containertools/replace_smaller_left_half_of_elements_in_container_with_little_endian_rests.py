from abjad.tools.containertools._replace_half_of_elements_in_container_with_rests import \
   _replace_half_of_elements_in_container_with_rests


def replace_smaller_left_half_of_elements_in_container_with_little_endian_rests(container):
   r'''.. versionadded:: 1.1.2

   For container `C` of even length `l` replace the first ``l/2`` elements
   of `C` with little-endian rests::

      abjad> staff = Staff(macros.scale(10))
      abjad> containertools.replace_smaller_left_half_of_elements_in_container_with_little_endian_rests(staff)
      abjad> f(staff)
      \new Staff {
         r8
         r2
         a'8
         b'8
         c''8
         d''8
         e''8
      }

   For container `C` of odd length `l` replace the first ``floor(l/2)`` elements
   of `C` with little-endian rests::

      abjad> staff = Staff(macros.scale(11))
      abjad> containertools.replace_smaller_left_half_of_elements_in_container_with_little_endian_rests(staff)
      abjad> f(staff)
      \new Staff {
         r8
         r2
         a'8
         b'8
         c''8
         d''8
         e''8
         f''8
      }
   '''

   return _replace_half_of_elements_in_container_with_rests(
      container, 'left', 'right', 'little-endian')

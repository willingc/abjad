'''Spacing tools.

   This package depends on only the core *Abjad* classes.'''

from abjad.tools.importtools.package_import import _package_import

_package_import(__path__[0], globals( ))

from SpacingIndication import SpacingIndication

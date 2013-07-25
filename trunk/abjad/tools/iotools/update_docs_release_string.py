import os
from abjad.tools import configurationtools


def update_docs_release_string():
    from abjad import abjad_configuration
    docs_conf_file_name = os.path.join(
        abjad_configuration.abjad_directory_path, 'docs', 'conf.py')
    docs_conf_file = file(docs_conf_file_name, 'r')
    output_lines = []
    for input_line in docs_conf_file.readlines():
        if input_line.startswith('release ='):
            abjad_revision_string = \
                configurationtools.get_abjad_revision_string()
            output_lines.append("release = '%s'\n" % abjad_revision_string)
        else:
            output_lines.append(input_line)
    docs_conf_file.close()
    docs_conf_file = file(docs_conf_file_name, 'w')
    output_lines = ''.join(output_lines)
    docs_conf_file.write(output_lines)
    docs_conf_file.close()
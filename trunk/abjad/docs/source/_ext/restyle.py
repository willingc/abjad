import importlib
import inspect
import types

from docutils import nodes

from sphinx import addnodes


def doctree_read(app, doctree):

    for desc_node in doctree.traverse(addnodes.desc):
        if desc_node.get('domain') != 'py':
            continue

        signature_node = desc_node.traverse(addnodes.desc_signature)[0]
        module_name = signature_node.get('module')
        object_name = signature_node.get('fullname')
        object_type = desc_node.get('objtype')

        if object_type == 'class':
            module = importlib.import_module(module_name)
            cls = getattr(module, object_name, None)
            if cls is None:
                continue
            addname_node = signature_node.traverse(addnodes.desc_addname)[0]
            text = addname_node[0].astext()
            parts = [x for x in text.split('.') if x]
            if parts[0] in ('abjad', 'experimental'):
                parts = parts[2:-2]
            text = '{}.'.format('.'.join(parts))
            addname_node[0] = nodes.Text(text)
            if inspect.isabstract(cls):
                labelnode = addnodes.only(expr='html')
                labelnode.append(nodes.literal(
                    '',
                    'abstract',
                    classes=['attribute', 'abstract'],
                    ))
                signature_node.insert(0, labelnode)

        elif object_type in ('method', 'attribute', 'staticmethod', 'classmethod'):
            object_parts = object_name.split('.')
            module = importlib.import_module(module_name)                
            cls_name, attr_name = object_name.split('.') 
            cls = getattr(module, cls_name, None)
            if cls is None:
                continue
            attr = getattr(cls, attr_name)
            label_node = addnodes.only(expr='html')
            if getattr(attr, '__isabstractmethod__', False):
                label_node.append(nodes.literal(
                    '',
                    'abstract',
                    classes=['attribute', 'abstract'],
                    ))
            if isinstance(attr, types.FunctionType):
                # remove Sphinx's annotation, so we can use our own.
                signature_node.pop(0)
                label_node.append(nodes.literal(
                    '',
                    'staticmethod',
                    classes=['attribute', 'staticmethod'],
                    ))
            elif hasattr(attr, 'im_self') and attr.im_self is not None:
                signature_node.pop(0)
                label_node.append(nodes.literal(
                    '',
                    'classmethod',
                    classes=['attribute', 'classmethod'],
                    ))
            signature_node.insert(0, label_node)

        #else:
        #    print
        #    print object_name, object_type
        

def setup(app):
    app.connect('doctree-read', doctree_read)
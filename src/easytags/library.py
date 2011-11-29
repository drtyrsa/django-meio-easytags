# -*- coding: utf-8 -*-

'''
Created on 01/03/2011

@author: vbmendes
'''

from django.template import Library

from node import EasyNode, EasyAsNode, EasyIncNode

class EasyLibrary(Library):

    @classmethod
    def _get_name_and_renderer(cls, name, renderer):
        if not renderer:
            renderer = name
            name = renderer.__name__
        return name, renderer

    def easytag(self, name = None, renderer = None):
        return self._handle_decorator(EasyNode, name, renderer)

    def easyastag(self, name = None, renderer = None):
        return self._handle_decorator(EasyAsNode, name, renderer)

    def easyinctag(self, name = None, renderer = None, **kwargs):
        if 'template_name' not in kwargs:
            raise TypeError('Named argument "template_name" is required')
        return self._handle_decorator(EasyIncNode, name, renderer, **kwargs)

    def _handle_decorator(self, node_class, name, renderer, **kwargs):
        if not name and not renderer:
            return self.easytag
        if not renderer:
            if callable(name):
                renderer = name
                return self._register_easytag(node_class, renderer.__name__, renderer, **kwargs)
            else:
                def dec(renderer):
                    return self._register_easytag(node_class, name, renderer, **kwargs)
                return dec
        return self._register_easytag(node_class, name, renderer, **kwargs)

    def _register_easytag(self, node_class, name, renderer, **kwargs):
        if not renderer:
            renderer = name
            name = renderer.__name__

        def render_context(self, context, *args, **kwargs):
            return renderer(context, *args, **kwargs)

        get_argspec = classmethod(lambda cls: node_class.get_argspec(renderer))

        class_dict = {
            'render_context': render_context,
            'get_argspec': get_argspec,
        }

        if 'template_name' in kwargs:
            class_dict['template_name'] = kwargs['template_name']
            class_dict['takes_context'] = kwargs.get('takes_context', False)

        tag_node = type('%sEasyNode' % name, (node_class,), class_dict)
        self.tag(name, tag_node.parse)
        return renderer

# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedTuple(TypedCollection):

    ### CLASS VARIABLES ### 

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        TypedCollection.__init__(self, 
            item_class=item_class, 
            name=name,
            tokens=tokens,
            )
        tokens = tokens or []
        self._collection = tuple(self._item_callable(token) 
            for token in tokens)

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        r'''Change `token` to item and return true if item exists in
        collection.
        '''
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __getitem__(self, i):
        '''Aliases tuple.__getitem__().
        '''
        return self._collection[i]

    def __reversed__(self):
        '''Aliases tuple.__reversed__().
        '''
        return self._collection.__reversed__()

    ### PUBLIC METHODS ###

    def count(self, token):
        r'''Change `token` to item and return count in collection.
        '''
        item = self._item_callable(token)
        return self._collection.count(item)

    def index(self, token):
        r'''Change `token` to item and return index in collection.
        '''
        item = self._item_callable(token)
        return self._collection.index(item)

import abc
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class SettingLookupExpression(AnchoredExpression, PayloadCallbackMixin):
    r'''SetExpression lookup.

    Look up `attribute` setting active at `offset` in `voice_name`.

    SetExpression is assumed to resolve to a list or other iterable payload.

    Because of this setting lookups afford payload callbacks.

    Composers create concrete setting lookup classes during specification.

    Composers create concrete setting lookup classes with lookup methods.

    All lookup methods implement against ``OffsetExpression``.
    '''

    ### INITIALIZER ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, voice_name=None, offset=None, callbacks=None):
        from experimental.tools import expressiontools
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(offset, expressiontools.OffsetExpression)
        AnchoredExpression.__init__(self, anchor=offset)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._attribute = attribute
        self._voice_name = voice_name
        self._offset = offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''SetExpression lookup attribute.

        Return string.
        '''
        return self._attribute

    @property
    def offset(self):
        '''SetExpression lookup offset.

        Return offset expression.
        '''
        return self._offset

    @property
    def voice_name(self):
        '''SetExpression lookup voice name.

        Return string.
        '''
        return self._voice_name

    ### PRIVATE METHODS ###
    
    @abc.abstractmethod
    def evaluate(self):
        pass

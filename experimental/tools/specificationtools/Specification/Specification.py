import abc
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import expressiontools


class Specification(AbjadObject):
    r'''Specification.

    Abstract base class from which score specification and 
    segment specification classes inherit.

    Interpreter interprets score and segment specifications.

    Abjad score object results from interpretation.

    Specification properties are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = expressiontools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_template):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        self._score_template = score_template
        self._score_model = score_template()
        self._abbreviated_context_names = []
        self._context_names = []
        self._multiple_context_settings = expressiontools.SetExpressionInventory()
        self._single_context_settings_by_context = specificationtools.ContextProxyDictionary(score_template())
        self._initialize_context_name_abbreviations()
        self._contexts = specificationtools.ContextProxyDictionary(score_template())
        self._single_context_settings = expressiontools.SetExpressionInventory()

    ### READ-ONLY PRIVATE PROPERTIES ###

    # TODO: remove in favor of SpecificationInterface._anchor_abbreviation
    @property
    def _anchor_abbreviation(self):
        '''Form of specification suitable for writing to disk.
        '''
        return self.specification_name

    def _context_name_to_parentage_names(self, context_name, proper=True):
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        if proper:
            parentage = componenttools.get_proper_parentage_of_component(context)
        else:
            parentage = componenttools.get_improper_parentage_of_component(context)
        context_names = [context.name for context in parentage]
        return context_names

    def _get_first_element_in_expr_by_parentage(self, expr, context_name, include_improper_parentage=False):
        context_names = [context_name]
        if include_improper_parentage:
            context_names = self._context_name_to_parentage_names(context_name, proper=False)
        for context_name in context_names:
            for element in expr:
                if element.context_name is None:
                    return element
                if element.context_name == context_name:
                    return element

    ### PRIVATE METHODS ###

    def _context_token_to_context_names(self, context_token):
        if context_token is None:
            context_names = None
        elif context_token == [self.score_name]:
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = [context_token.score_name]
        elif context_token in self._abbreviated_context_names:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all([
            x in self._abbreviated_context_names for x in context_token]):
            context_names = context_token
        elif isinstance(context_token, contexttools.Context):
            context_names = [context_token.name]
        elif contexttools.all_are_contexts(context_token):
            context_names = [context.name for context in context_token]
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names

    def _initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
            self._abbreviated_context_names.append(context_name)
        score = self.score_template()
        self._score_name = score.name
        for context in iterationtools.iterate_contexts_in_expr(score):
            if hasattr(context, 'name'):
                self._context_names.append(context.name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        return self._context_names

    @property
    def contexts(self):
        return self._contexts

    @property
    def multiple_context_settings(self):
        return self._multiple_context_settings

    @property
    def score_model(self):
        return self._score_model

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def single_context_settings(self):
        return self._single_context_settings

    @property
    def single_context_settings_by_context(self):
        return self._single_context_settings_by_context

    @property
    def timespan(self):
        return self._timespan

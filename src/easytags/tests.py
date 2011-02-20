
from django import template
from django.test import TestCase

from easytags.parser import get_args_kwargs_from_token_parse

class ParserTests(TestCase):

    def test_environment(self):
        """
            Just make sure everything is set up correctly.
        """
        self.assertTrue(True)

    def test_parse_tag_with_args(self):
        """
            Tests if the parser recognizes one tag and parses its args
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" "arg2"')
        self.assertEquals(
            {'args': ('"arg1"', '"arg2"'), 'kwargs': {}},
            get_args_kwargs_from_token_parse(parser, token)
        )
    
    def test_parse_tag_with_kwargs(self):
        """
            Tests if the parser recognizes one tag and parses its kwargs
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name kwarg1="1" kwarg2="2"')
        self.assertEquals(
            {'args': (), 'kwargs': {'kwarg1': '"1"', 'kwarg2': '"2"'}},
            get_args_kwargs_from_token_parse(parser, token)
        )
    
    def test_parse_tag_with_args_and_kwargs(self):
        """
            Tests if the parser recognizes one tag and parses its args and kwargs
        """
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name "arg1" kwarg1="1"')
        self.assertEquals(
            {'args': ('"arg1"',), 'kwargs': {'kwarg1': '"1"'}},
            get_args_kwargs_from_token_parse(parser, token)
        )

    def test_parse_tag_with_variable_arg(self):
        parser = template.Parser([])
        token = template.Token(template.TOKEN_BLOCK, 'tag_name argvariable')
        self.assertEquals(
            {'args': ('argvariable',), 'kwargs': {}},
            get_args_kwargs_from_token_parse(parser, token)
        )

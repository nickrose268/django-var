from django import template
import unittest
import re

register = template.Library()

@register.filter(name='dget')
def dget(value, args):
    """ Extracts values from 1 or 2 layered dictionary

    Args:
        value: The input value to be filter
        args: The string argument to the filter "xxx, yyy"

    Returns:
        The dictionary values corresponding to the given keys

    Setup:
        This file will be at in <project_name>/<app_name>/templatetags/local_tags.py
        In the template insert {% load local_tags %}

    Usage:
        Given the following dictionary
        {'1': {'11': '11', '12': '12', '13': '13'}, '2': {'21': '21', '22': '22', '23': '23'} }
        The followng syntax:
            {{my_dictionary|dget:'1,12'|<other filters, e.g. safe>}}
        will return
            '12'

    """
    args = re.sub('[\s]+','', args).split(',')
    if value.get(args[0]):
        if len(args) == 2:
            if value[args[0]].get(args[1]):
                return value[args[0]][args[1]]
            else:
                return ''
        return value[args[0]]
    return ''

@register.filter(name='wordswitch')
def wordswitch(value, args):
    """ Extracts values from 1 or 2 layered dictionary

    Args:
        value: The input value to be filter
        args: The string argument to the filter "word_tested, returned_if_true, returned_if_false"

    Returns:
        Another word depending on if the content of the tag variable is equal to the word being tested

    Setup:
        This file will be at in <project_name>/<app_name>/templatetags/local_tags.py
        In the template insert {% load local_tags %}

    Usage:
        The followng syntax:
            {{language|wordswitch:'dk, Kontakt mig, Contact me'|<other filters, e.g. safe>}}
        will return
            'Kontakt mig' if language = 'dk' and 'Contact me' if not (in theory one could add more arguments and have several languages)

    It may seem that this is putting too much logic into the templates, but it is only intended for lots of small phrases
    that you want to set up once and then forget!

    """
    args = re.sub('([\s]*,[\s]*)',',', args)
    args = re.sub('[\s]+$|^[\s]+','', args)
    args = args.split(',')
    if value == args[0]:
        return args[1]
    else:
        return args[2]

class TagTest(unittest.TestCase):
    """ Usage: python -m unittest local_tags """

    def test_dget(self):

        def check_dget(d1, args, expected):
            res = dget(d1, args)
            print(f'Testing if {res} is {expected}')
            self.assertEqual(res, expected)

        d1 =  {'1': {'11': '11', '12': '12', '13': '13'}, '2': {'21': '21', '22': '22', '23': '23'} }
        check_dget(d1, ' 1', d1['1'])
        check_dget(d1, '1, 12', d1['1']['12'])
        check_dget(d1, '3', '')
        check_dget(d1, '1,15', '')


    def test_wordswitch(self):

        def check_wordswitch(word, args, expected):
            res = wordswitch(word, args)
            print(f'Testing if {res} is {expected}')
            self.assertEqual(res, expected)

        check_wordswitch('dk', 'dk, Goddag, Hello', 'Goddag')
        check_wordswitch('en', 'dk, Goddag, Hello', 'Hello')
        check_wordswitch('en', 'dk, Goddag    ,   Hello   ', 'Hello')

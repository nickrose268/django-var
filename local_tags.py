from django import template
import unittest

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
    args = args.split(',')
    if value.get(args[0]):
        if len(args) == 2:
            if value[args[0]].get(args[1]):
                return value[args[0]][args[1]]
            else:
                return
        return value[args[0]]


class TagTest(unittest.TestCase):
    """ Usage: python -m unittest <this-file-without-the.py> """

    def test_dget(self):

        def check_dget(d1, args, expected):
            res = dget(d1, args)
            print(f'Testing if {res} is {expected}')
            self.assertEqual(res, expected)

        d1 =  {'1': {'11': '11', '12': '12', '13': '13'}, '2': {'21': '21', '22': '22', '23': '23'} }
        check_dget(d1, '1', d1['1'])
        check_dget(d1, '1,12', d1['1']['12'])
        check_dget(d1, '3', None)
        check_dget(d1, '1,15', None)

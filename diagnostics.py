import unittest

def inspect_me(ret):
    """ Inspection function for django

        Args: ret, you can put anything in here that you want to spit out, but
              typically it could be the return value of a super() call.

        Usage: Put it in a function that you want to inspect  for example like this:
                        def clean(self, *args, **kwargs):
                            ret=super().clean()
                            inspect_me(ret)
                            return ret

        Why is it not a decorator?
        It seems an obvious candidate to be a decorator, but this wont work because it
        will consider everything from its own (the decorator's) point of view.

    """

    import inspect
    import re
    print('*'*50)
    stack = inspect.stack()
    this_file = re.findall('[^\\\]*$', stack[1][1])[0]
    this_class = stack[1][0].f_locals["self"].__class__
    #this_method = stack[1][0].f_code.co_name
    this_method = stack[1][3]
    calling_class = stack[2][0].f_locals["self"].__class__
    #calling_method = stack[2][0].f_code.co_name
    calling_method = stack[2][3]
    print(f'IN FUNCTION: {this_method} \
        \nThis file: {this_file} \
        \nThis class: {this_class} \
        \nThis method: {this_method} \
        \nCalling class: {calling_class} \
        \nCalling method: {calling_method} \
        \nReturn type: {type(ret)} \
        \nReturn value: {ret} \
        ')
    print('*'*50)
    return this_file, this_class, this_method, calling_class, calling_method


class InspectTest(unittest.TestCase):
    """ Usage: python -m unittest <this-file-without-the.py> """

    class MyClass(unittest.TestCase):
        def test_do_the_test(self):
            this_file, this_class, this_method, calling_class, calling_method\
                                                    = inspect_me('Hello there!')
            print(f'Testing if "{this_file}" is "diagnostics.py"')
            self.assertEqual(this_file, 'diagnostics.py')
            print(f'Testing if "{this_class}" is "<class \'diagnostics.InspectTest.MyClass\'>"')
            self.assertEqual(str(this_class), "<class 'diagnostics.InspectTest.MyClass'>")
            print(f'Testing if "{this_method}" is "test_do_the_test"')
            self.assertEqual(this_method, 'test_do_the_test')
            print(f'Testing if "{calling_class}" is "<class \'diagnostics.InspectTest\'>"')
            self.assertEqual(str(calling_class), "<class 'diagnostics.InspectTest'>")
            print(f'Testing if "{calling_method}" is "test_inspect_me"')
            self.assertEqual(calling_method, 'test_inspect_me')

    def test_inspect_me(self):
        c = self.MyClass()
        c.test_do_the_test()

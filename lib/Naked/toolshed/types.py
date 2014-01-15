#!/usr/bin/env python

##TODO : try/catch around the getter methods in case they are missing

#------------------------------------------------------------------------------
# [ NakedObject class ]
#   A generic Python object
#   Assigns object attributes by key in the dictionary argument
#------------------------------------------------------------------------------
class NakedObject:
    # initialize with an attributes dictionary {attribute_name, attribute_value}
    def __init__(self, attributes={}):
        if len(attributes) > 0:
            self._addAttributes(attributes)
        from sys import version_info
        self.py_version = (version_info[0], version_info[1], version_info[2])  # add python version as metadata to the object

    #------------------------------------------------------------------------------
    # [ _addAttributes method ] (no return value)
    #  sets the attributes on a NakedObject or inherited type with the `attributes` dictionary
    #------------------------------------------------------------------------------
    def _addAttributes(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])

    #------------------------------------------------------------------------------
    # [ _getAttributeDict method ] (dictionary)
    #  returns a dictionary of the NakedObject instance attributes
    #------------------------------------------------------------------------------
    def _getAttributeDict(self):
        return self.__dict__

    #------------------------------------------------------------------------------
    # [ getAttribute method ] (attribute dependent type)
    #  returns the respective attribute for the `attribute` name on the NakedObject instance
    #------------------------------------------------------------------------------
    def getAttribute(self, attribute):
        return getattr(self, attribute)

    #------------------------------------------------------------------------------
    # [ setAttribute method ] (no return value)
    #  sets a NakedObject attribute `value` for the `attribute` name
    #------------------------------------------------------------------------------
    def setAttribute(self, attribute, value):
        setattr(self, attribute, value)

    #------------------------------------------------------------------------------
    # [ hasAttribute method ] (boolean)
    #  returns truth test for presence of an `attribute` name on the NakedObject
    #------------------------------------------------------------------------------
    def hasAttribute(self, attribute):
        return hasattr(self, attribute)

#------------------------------------------------------------------------------
# [ XDict class ]
#   An inherited extension to the dictionary object that permits attachment of attributes
#------------------------------------------------------------------------------
class XDict(dict, NakedObject):
    def __init__(self, dict_obj, attributes={}):
        dict.__init__(self, dict_obj)
        NakedObject.__init__(self, attributes)

    #------------------------------------------------------------------------------
    # XDict Operator Overloads
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    #  +- overload extends XDict with another dictionary
    #  overwrites existing keys with another_dict (right sided argument) keys if they are the same
    #  returns the updated XDict object
    #------------------------------------------------------------------------------
    def __iadd__(self, another_dict):
        self.update(another_dict)
        return self

    #------------------------------------------------------------------------------
    # << overload extends XDict with another dictionary
    #  overwrites existing keys with another_dict (right sided argument) keys if they are the same
    #  modifies the XDict in place, no return value
    #------------------------------------------------------------------------------
    def __lshift__(self, another_dict):
        self.update(another_dict)


    #------------------------------------------------------------------------------
    # Value Methods
    #------------------------------------------------------------------------------
    # return XTuple of minimum value
    def min_val(self):
        result = min(zip(self.values(), self.keys()))
        return XTuple( result, {'val': result[0], 'key': result[1]})

    # return XTuple of maximum value
    def max_val(self):
        result = max(zip(self.values(), self.keys()))
        return XTuple( result, {'val': result[0], 'key': result[1]} )

    # sum values
    def sum_vals(self):
        return sum(self.values())

    # map a function to every value in the dictionary
    def map_to_vals(self, the_func):
        return XDict( zip(self, map(the_func, self.values())), self._getAttributeDict())

    #------------------------------------------------------------------------------
    # Comparison Methods
    #------------------------------------------------------------------------------
    def intersection(self, another_dict):
        return self.keys() & another_dict.keys()

    def difference(self, another_dict):
        return self.keys() - another_dict.keys()


    #------------------------------------------------------------------------------
    # [ iter method ] (tuple of each key and value in dictionary)
    #   Generator method that returns tuples of key, value in dictionary
    #   uses appropriate method from Python 2 and 3
    #------------------------------------------------------------------------------
    def iter(self):
        if self.py_version[0] > 2:
            return self.items()
        else:
            return self.iteritems()

#------------------------------------------------------------------------------
# [ XList class ]
#  An inherited extension to the list object that permits attachment of attributes
#------------------------------------------------------------------------------
class XList(list, NakedObject):
    def __init__(self, list_obj, attributes={}):
        list.__init__(self, list_obj)
        NakedObject.__init__(self, attributes)

    #------------------------------------------------------------------------------
    # Operator Overloads/Defs
    #------------------------------------------------------------------------------

    #   += operator overload to extend the XList with the argument list
    def __iadd__(self, another_list):
        self.extend(another_list)
        return self

    #   >> operator is overloaded to extend the argument list with the XList
    def __rshift__(self, another_list):
        another_list.extend(self)
        return another_list

    #   << operator is overloaded to extend the XList with the argument list
    def __lshift__(self, another_list):
        self.extend(another_list)
        return self

    #------------------------------------------------------------------------------
    # XList Methods
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # XList String Methods
    #------------------------------------------------------------------------------
    # [ join method ] (string)
    #  Concatenate strings in the list and return
    #  Default separator between string list values is an empty string
    #  Pass separator character(s) as an argument to the method
    #------------------------------------------------------------------------------
    def join(self, separator=""):
        return separator.join(self)

    #------------------------------------------------------------------------------
    # [ prefix method ] (list of strings)
    #  Prepend a string to each list item string
    #------------------------------------------------------------------------------
    def prefix(self, before):
        return [ "".join([before, x]) for x in self ]

    #------------------------------------------------------------------------------
    # [ postfix method ] (list of strings)
    #  Append a string to each list item string
    #------------------------------------------------------------------------------
    def postfix(self, after):
        return [ "".join([x, after]) for x in self ]

    #------------------------------------------------------------------------------
    # [ surround method ] (list of strings)
    #  Surround each list item with a before and after string argument passed to the method
    #------------------------------------------------------------------------------
    def surround(self, before, after):
        return [ "".join([before, x, after]) for x in self ]

    # Numeric methods
    def max(self):
        return max(self)

    def min(self):
        return min(self)

    def sum(self):
        return sum(self)

    # remove duplicate items in an XList
    def remove_duplicates(self):
        return XList( set(self), self._getAttributeDict() )

    # map a function to every item in the XList
    def map_to_items(self, the_func):
        return XList( map(the_func, self), self._getAttributeDict())

    #------------------------------------------------------------------------------
    # Conversion Methods
    #------------------------------------------------------------------------------
    # [ ndarray method ] (Numpy ndarray object)
    #  returns a Numby ndarray object by conversion from the XList object
    #  user must have Numpy installed or ImportError is raised
    #------------------------------------------------------------------------------
    def ndarray(self):
        try:
            import numpy as np
            return np.array(self)
        except ImportError as ie:
            if DEBUG_FLAG:
                sys.stderr.write("Naked Framework Error: unable to return base filename from filename() function (Naked.toolshed.system).")
            raise ie

    def xset(self):
        attr_dict = self._getAttributeDict()
        return XSet(set(self), attr_dict)

    def xfset(self):
        attr_dict = self._getAttributeDict()
        return XFSet(set(self), attr_dict)

    #------------------------------------------------------------------------------
    # XList Iterables
    #------------------------------------------------------------------------------
    # [ chain_iter method ] (iterable items of type contained in multiple list arguments)
    #   Generator that returns iterable for each item in the multiple list arguments in sequence (does not require new list)
    #------------------------------------------------------------------------------
    def chain_iter(self, *lists):
        from itertools import chain
        return chain(*lists)


#------------------------------------------------------------------------------
# [ XPriorityQueue class ]
#
#------------------------------------------------------------------------------
import heapq
class XPriorityQueue(NakedObject):
    def __init__(self, initial_iterable=[], attributes={}):
        NakedObject.__init__(self, attributes)
        self._queue = []
        self._index = 0

    # O(log n) complexity
    def push(self, the_object, priority):
        heapq.heappush(self._queue, (-priority, self._index, the_object))
        self._index += 1

    # O(log n) complexity
    def pop(self):
        return heapq.heappop(self._queue)[-1]


#------------------------------------------------------------------------------
# [ XQueue class ]
#
#------------------------------------------------------------------------------
from collections import deque
class XQueue(deque, NakedObject):
    def __init__(self, initial_iterable=[], attributes={}, max_length=10):
        deque.__init__(self, initial_iterable, max_length)
        NakedObject.__init__(self, attributes)


#------------------------------------------------------------------------------
# [ XSet class ]
#  An inherited extension to the mutable set object that permits attribute assignment
#  Inherits from set and from NakedObject (see methods in NakedObject at top of this module
#------------------------------------------------------------------------------
class XSet(set, NakedObject):
    def __init__(self, set_obj, attributes={}):
        set.__init__(self, set_obj)
        NakedObject.__init__(self, attributes)

    #   << operator is overloaded to extend the XSet with a second set
    def __lshift__(self, another_set):
        self.update(another_set)
        return self

    #   += operator overload to extend the XSet with a second set
    def __iadd__(self, another_set):
        self.update(another_set)
        return self

    def xlist(self):
        attr_dict = self._getAttributeDict()
        return XList(list(self), attr_dict)

    def xfset(self):
        attr_dict = self._getAttributeDict()
        return XFSet(self, attr_dict)

#------------------------------------------------------------------------------
# [ XFSet class ]
#  An inherited extension to the immutable frozenset object that permits attribute assignment
#  Immutable so there is no setter method, attributes must be set in the constructor
#------------------------------------------------------------------------------
class XFSet(frozenset):
    def __new__(cls, the_set, attributes={}):
        set_obj = frozenset.__new__(cls, the_set)
        if len(attributes) > 0:
            for key in attributes:
                setattr(set_obj, key, attributes[key])
        from sys import version_info
        set_obj.py_version = (version_info[0], version_info[1], version_info[2]) #add python interpreter version to the object
        return set_obj

    def _getAttributeDict(self):
        return self.__dict__

    def getAttribute(self, attribute):
        return getattr(self, attribute)

    def xlist(self):
        attr_dict = self._getAttributeDict()
        return XList(list(self), attr_dict)

    def xset(self):
        attr_dict = self._getAttributeDict()
        return XSet(self, attr_dict)

#------------------------------------------------------------------------------
# [ XString class ]
#   An inherited extension to the immutable string object that permits attributes
#   Immutable so there is no setter method, attributes must be set in the constructor
#------------------------------------------------------------------------------
class XString(str):
    def __new__(cls, string_text, attributes={}):
        str_obj = str.__new__(cls, string_text)
        if len(attributes) > 0:
            for key in attributes:
                setattr(str_obj, key, attributes[key])
        from sys import version_info
        str_obj.py_version = (version_info[0], version_info[1], version_info[2]) #add python version as metadata to the object
        return str_obj

    def getAttribute(self, attribute):
        return getattr(self, attribute)

    # fastest substring search truth test
    def contains(self, substring):
        return substring in self

#------------------------------------------------------------------------------
# [ XTuple class ]
#
#------------------------------------------------------------------------------
class XTuple(tuple):
    def __new__(cls, the_tuple, attributes={}):
        tup_obj = tuple.__new__(cls, the_tuple)
        if len(attributes) > 0:
            for key in attributes:
                setattr(tup_obj, key, attributes[key])
        from sys import version_info
        tup_obj.py_version = (version_info[0], version_info[1], version_info[2])
        return tup_obj




if __name__ == '__main__':
    pass
    # nl = XList(['a', 'b', 'c'], {"version":"1.0.1", "test":"code"})
    # nl << ['d', 'e', 'f']
    # the_list = list(range(5000))
    # nl = XList(the_list)
    # nq = XPriorityQueue()
    # nq.push('test', 5)
    # nq.push('one', 3)
    # nq.push('another', 4)
    # print(nq.pop())
    # print(nq.pop())
    # print(nq.pop())

    # nl = XList(['test', 'test', 'another'], {'p': 'attribute'})
    # print(nl)
    # nl = nl.remove_dupes()
    # print(nl)
    # nq = XQueue(nl, max_length=2)
    # print(nq)

    # xs = XSet({'test', 'true', 'false'}, {'bonus': 'candy', 'test': 'another'})
    # xs += {'bogus', 'yep'}
    # print(xs)

    # xd = XDict({'test': 'testing', 'another': 'yep'}, {'a': '1', 'b': '2'})
    # ad = {'test': 'yes', 'is':'more'}
    # xd << ad
    # print(xd)

    # xstr = XString("This is a really long string that contains a few cool things.")
    # xstr.contains('few')

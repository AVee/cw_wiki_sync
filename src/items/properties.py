'''
Created on 10 Nov 2019

@author: AVee
'''
from distutils.util import strtobool

class Property(object):
    def __init__(self, json_name: str, default = None, mandatory = False):
        super().__init__()
        self.json_name = json_name
        self._default = default
        self._value = default
        self._mandatory = mandatory
        self._dirty = False
        
    @property
    def value(self):
        return self._get_value()

    def _get_value(self):
        return self._value

    @value.setter    
    def value(self, value):
        self._set_value(value)
    
    def _set_value(self, value):
        if value != self._value:
            self._value = value
            self._dirty = True
                
    def get_wiki_value(self):
        return None if self._value == None else str(self._value)
    
    def __str__(self):
        s = self.get_wiki_value()
        return str(s) if s != '' else 'None'
    
    def __eq__(self, other):
        if isinstance(other, Property):
            if type(other) == type(self):
                return self.value == other.value
            else:
                return False
        return  NotImplemented            

class BoolProperty(Property):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        
    def _set_value(self, value):
        if value == 'None':
            value = None
            
        if value != None:
            value = False if strtobool(str(value)) == 0 else True
        super()._set_value(value)
    
    def get_wiki_value(self):
        value = super().value
        return None if value == None else 'Yes' if value else 'No'
    
class IntProperty(Property):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
    
    def _set_value(self, value):
        if value == None:
            value = None
        else:
            value = int(value)
        super()._set_value(value)

class LinkProperty(Property):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

class SetProperty(Property):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

class SetListProperty(Property):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)

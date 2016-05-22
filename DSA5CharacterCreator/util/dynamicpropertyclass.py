
from PyQt5.QtCore import QObject, pyqtWrapperType, pyqtProperty, pyqtSignal

class DynamicPropertyClass(object):
    _noneInitList = []

    def __new__(cls, *args, **kwargs):
        obj = super(DynamicPropertyClass, cls).__new__(cls)
        for prop in cls._noneInitList:
            setattr(obj, prop, None)
        return obj

    @classmethod
    def addProperty(cls, name):
        member = "_" + name
        cls._noneInitList.append(member)
        getter = lambda self: getattr(self, member)
        getter.__name__ = name
        setter = lambda self, value: setattr(self, member, value)
        setter.__name__ = name
        setattr(cls, name, property(getter, setter))
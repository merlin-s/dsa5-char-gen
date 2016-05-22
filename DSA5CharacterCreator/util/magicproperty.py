# -*- coding: utf-8 -*-
# https://gist.github.com/mrzechonek/bd7c059b5742a9c1a7fd#file-magic-py
# https://gist.github.com/merlin-s/2577e9f774eb3bd3a37f

from PyQt5.QtCore import QObject, pyqtWrapperType, pyqtProperty, pyqtSignal


class magicProperty:
    """
        Just a placeholder, it gets replaced with pyqtProperty
        when creating the object. Used to customise signal name.
    """

    def __init__(self, property_type, signal=None):
        self.property_type = property_type
        self.signal = signal


class magicWrapperType(pyqtWrapperType):
    @staticmethod
    def magic_property(prop_name, prop_type, notify, notify_name):
        """
            Create pyqtProperty object with value captured in the closure
            and a 'notify' signal attached.
            You need to pass both:
                - unbound signal, because pyqtProperty needs it
                - signal name to allow setter to find the *bound* signal
                  and emit it.
        """

        def getter(self):
            value = getattr(self, '_' + prop_name)
            return value

        def setter(self, value):
            setattr(self, '_' + prop_name, value)
            getattr(self, notify_name).emit(value)

        prop = pyqtProperty(
            type=prop_type,
            fget=getter,
            fset=setter,
            notify=notify)

        return prop

    def __new__(mcs, name, bases, dct):
        def handleDict(dct, setattr):
            # don't touch attributes other than magicProperties
            properties = list(
                filter(
                    lambda i: isinstance(i[1], magicProperty),
                    dct.items()
                )
            )
            for property_name, p in properties:
                signal = pyqtSignal(p.property_type)
                signal_name = p.signal or property_name + "_changed"

                # create dedicated signal for each property
                setattr(signal_name, signal)

                # substitute magicProperty placeholder with real pyqtProperty
                setattr(property_name, magicWrapperType.magic_property(
                    property_name,
                    p.property_type,
                    signal,
                    signal_name
                ))

        handleDict(dct, lambda n, v: dct.update({n: v}))

        @classmethod
        def handleClsDict(cls):
            handleDict(cls.__dict__, lambda n, v: setattr(cls, n, v))

        dct['initMagicObjectClass'] = handleClsDict
        return super().__new__(mcs, name, bases, dct)


class MagicObject(QObject, metaclass=magicWrapperType):
    pass

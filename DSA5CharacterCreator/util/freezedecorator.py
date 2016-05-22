def freezeWithArgs(cls, freezeValues):
    _init = cls.__init__

    def init(self, *args, **kw):
        dpre = set(dir(self))
        _init(self, *args, **kw)
        cls.__setattr__(self, 'freeze', False)
        __frozenAttributes = set(dir(self)).difference(dpre)

        def assertFrozenAttrs():
            for a in __frozenAttributes:
                assert getattr(self, a) is not None, '%s is None' % a
        self.assertFrozenAttrs = assertFrozenAttrs
        cls.__setattr__(self, 'freeze', True)
        assert getattr(self, "freeze", False)
    cls.__init__ = init

    def _setattr(self, attr, value):
        if attr != 'freeze':
            frozen = getattr(self, 'freeze', False)
            if frozen and (freezeValues or not hasattr(self, attr)):
                raise AttributeError("You shall not add attributes!")
        super(cls, self).__setattr__(attr, value)
        assert getattr(self, attr) is value
    cls.__setattr__ = _setattr

    return cls


def freezeAttributeSet(cls):
    return freezeWithArgs(cls, freezeValues=False)


def freezeAttributes(cls):
    return freezeWithArgs(cls, freezeValues=True)

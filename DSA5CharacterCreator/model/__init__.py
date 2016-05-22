import logging
from collections import OrderedDict
from enum import Enum, unique

from PyQt5 import QtQml
from PyQt5.QtQml import QQmlListProperty

from util.freezedecorator import freezeAttributeSet
from util.magicproperty import MagicObject, magicProperty

logger = logging.getLogger(__name__)

__all__ = ['Trait', 'Perk', 'Quirk', 'TraitStatusEnum', 'AttributeEnum', 'Attribute', 'Species']


class Id(object):
    def __init__(self, override=None):
        self._name = override if override else ""

    def __str__(self):
        return self._name.__str__()

    def __repr__(self):
        return '%s (%s)' % (self._name.__repr__(), id(self))


class IdType(object):
    def __init__(self, identifier):
        super(IdType, self).__init__()
        assert isinstance(identifier, Id)
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier

    def __str__(self):
        return self._identifier.__str__()

    def __repr__(self):
        return self._identifier.__repr__()


@unique
class AttributeEnum(Enum):
    MU = ('MU', 'Mut')
    KL = ('KL', 'Klugheit')
    IN = ('IN', 'Intelligenz')
    CH = ('CH', 'Charisma')
    FF = ('FF', 'Fingerfertigkeit')
    GE = ('GE', 'Geschicklichkeit')
    KO = ('KO', 'Kondition')
    KK = ('KK', 'Körperkraft')

    def __init__(self, short, long):
        self.short = short
        self.long = long

    def __str__(self):
        return str(self.short)


class Attribute:
    def __init__(self, attributeid, value):
        self.attributeid = attributeid
        self.value = value


@unique
class TraitStatusEnum(Enum):
    # level 0
    FORBIDDEN = 0
    # level 0-III:
    UNUSUAL = 1
    NORMAL = 2
    USUAL = 3
    # level I-III
    OBLIGATORY = 4


class TraitDB:
    def __init__(self, parentDB=None):
        self._uuid_traits = OrderedDict()
        self._name_traits = OrderedDict()
        self._parentReg = parentDB.reg if parentDB else lambda x: None

    def get(self, name, uuid=None):
        if uuid:
            r = self._uuid_traits.get(uuid)
            assert r.name == name, name
            return r
        r = self._name_traits.get(name)
        if not r:
            logger.error('TraitDB failed to get value for get(name="%s",uuid="%s")', name, uuid)
        return r

    def reg(self, trait):
        self._parentReg(trait)
        assert trait.name not in self._name_traits
        assert trait.uuid not in self._uuid_traits
        self._uuid_traits[trait.uuid] = trait
        self._name_traits[trait.name] = trait
        return trait


class Trait(MagicObject):
    traitdb = TraitDB()
    name = magicProperty(str)
    cost = magicProperty(int)
    uuid = magicProperty(str)

    @classmethod
    def fromDB(cls, key):
        return cls.traitdb.get(key)

    def __init__(self, parent=None):
        super(Trait, self).__init__(parent)
        self.conditions = []

    def __str__(self):
        return "%s(%s, cost=%s)" % (
            self.__class__.__name__,
            self.name,
            self.cost
        )

    def __repr__(self):
        return self.__str__()


class Perk(Trait):
    db = TraitDB(Trait.traitdb)

    def __init__(self, name, uuid, cost, parent=None):
        super(Perk, self).__init__(parent)
        self.name = name
        self.uuid = uuid
        self.cost = cost

    @classmethod
    def fromDB(cls, key):
        return cls.db.get(key)


class Quirk(Trait):
    db = TraitDB(Trait.traitdb)

    def __init__(self, name, uuid, cost, parent=None):
        super(Quirk, self).__init__(parent)
        self.name = name
        self.uuid = uuid
        self.cost = cost

    @classmethod
    def fromDB(cls, key):
        return cls.db.get(key)


@freezeAttributeSet
class Species(MagicObject, IdType):
    name = magicProperty(str)
    cost = magicProperty(int)
    baseLE = magicProperty(int)
    baseSK = magicProperty(int)
    baseZ = magicProperty(int)
    baseGS = magicProperty(int)
    perkList = magicProperty(QQmlListProperty)

    def __init__(self, parent, identifier):
        super(Species, self).__init__(parent=parent, identifier=identifier)
        self.name = None
        self.cost = None
        self.baseLE = None
        self.baseSK = None
        self.baseZ = None
        self.baseGS = None
        self.talentBoniList = None
        self.cultureList = None
        self.perkList = None
        self.quirkList = None
        self.unusualPerkList = None
        self.unusualQuirkList = None
        self.hairColorList = None
        self.eyeColorList = None
        self.heightLimits = None
        self.weightLimits = None

    def select(self, c):
        c.species = self

    def deselect(self, c):
        pass


QtQml.qmlRegisterType(Species, 'dsa5', 1, 0, 'species')
QtQml.qmlRegisterType(Trait, 'dsa5', 1, 0, 'trait')
QtQml.qmlRegisterType(Perk, 'dsa5', 1, 0, 'perk')
QtQml.qmlRegisterType(Quirk, 'dsa5', 1, 0, 'quirk')
# QtQml.qmlRegisterType(Id, 'dsa5', 1, 0, 'id')

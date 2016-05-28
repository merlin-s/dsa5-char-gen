import logging
from collections import defaultdict

from PyQt5.QtCore import pyqtSlot, QVariant
from PyQt5.QtQml import qmlRegisterType

from translate import tr
import model
from util import *

logger = logging.getLogger(__name__)


class NameValuePair(MagicObject):
    name = magicProperty(str)
    value = magicProperty(str)

    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.name = name
        self.value = value

    def __str__(self):
        return '%s: "%s"' % (self.name, self.value)


def get_name_value_pair_list(parent, **kwargs):
    ret = list()
    for k, v in kwargs.items():
        setattr(parent, k, v)
        ret.append(NameValuePair(parent, name=tr(k), value=v))
    return ret


@freezeAttributeSet
class Character(MagicObject):
    name = magicProperty(str)
    ap = magicProperty(int)
    species = magicProperty(model.Species)
    selectionHandlers = None

    family = magicProperty(str)
    birthDate = magicProperty(str)
    birthLocation = magicProperty(str)
    culture = magicProperty(str)
    height = magicProperty(str)
    weight = magicProperty(str)
    gender = magicProperty(str)
    hairColor = magicProperty(str)
    eyeColor = magicProperty(str)
    title = magicProperty(str)
    socialStatus = magicProperty(str)
    basicData = magicProperty(QVariant)
    appearance = magicProperty(QVariant)

    @classmethod
    def initClass(cls):
        for b in model.AttributeEnum:
            setattr(cls, b.short, magicProperty(int))
        cls.initMagicObjectClass()
        for b in model.AttributeEnum:
            setattr(cls, b.short, 0)
        cls.selectionHandlers = {
            model.Perk: cls.onTraitChanged,
            model.Quirk: cls.onTraitChanged
        }

    def __init__(self, parent=None):
        super(Character, self).__init__(parent)
        self.name = "Horst"
        self.species = None
        self.traitLevels = defaultdict(int)
        self.traitStatus = defaultdict(lambda: model.TraitStatusEnum.NORMAL)
        self.ap = 1000
        self.basicData = get_name_value_pair_list(
            self,
            family="",
            birthDate="",
            birthLocation="",
            gender="männlich",
            title="Horst",
            socialStatus="profi",
        )
        self.appearance = get_name_value_pair_list(
            self,
            culture="",
            height="6 Fuß",
            weight="15 Stein",
            hairColor="rot",
            eyeColor="grün",
        )
        pass

    def characterCheck(self):
        pass

    def onTraitChanged(self, trait, selected):
        mode = selected != isinstance(trait, model.Perk)
        self.ap += trait.cost if mode else -trait.cost
        if selected:
            ok = True
            for c in trait.conditions:
                cok = c.eval(self)
                ok = ok and cok
                logger.info("checking %s --> %s", c, "ok" if cok else "failed")
            if ok:
                self.traitLevels[trait] = 1
            else:
                self.traitLevels[trait] = 0
                logger.info("check failed")
        else:
            self.traitLevels[trait] = 0

    @pyqtSlot(QObject, bool)
    def onSelectionChanged(self, c, selected):
        logger.info("%s %s", "selected:  " if selected else "deselected:", c)
        try:
            handler = self.selectionHandlers[c.__class__]
        except KeyError:
            return
        handler(self, c, selected)


qmlRegisterType(Character, 'dsa5', 1, 0, 'character')
qmlRegisterType(NameValuePair, 'dsa5', 1, 0, 'name_value_pair')
Character.initClass()

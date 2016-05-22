import logging

from PyQt5.QtQml import QQmlListProperty

import conditionchecks
import globals as g
import xmlutils
from model import Species, Id, Quirk, Perk

logger = logging.getLogger(__name__)


def _pTraits(cls, filename, xpath, delayedInits):
    xml = xmlutils.parseAndValidateXML(filename)
    traitList = xml.xpath(xpath)
    for xtrait in traitList:
        name = xtrait.get('name')
        trait_id = xtrait.get('id')
        try:
            cost = int(xtrait.get('cost') or 0)
        except ValueError:
            logger.error('cost invalid for trait %s' % name)
            cost = 0
        trait = cls(name, trait_id, cost, g.getApp())

        def delayedInitializeConditionChecks(trait=trait, xtrait=xtrait):
            conditions = conditionchecks.ConditionCheck.xmlParse(xtrait, 'trait "%s"' % trait.name)
            if conditions:
                trait.conditions = [condition for condition in conditions]
            if len(trait.conditions):
                logger.info('trait "%s": %s condition(s)', trait, len(trait.conditions))

        delayedInits.append(delayedInitializeConditionChecks)
        yield trait


def _pQuirks(cls, delayedInits):
    return map(cls.db.reg, _pTraits(cls, "quirks.xml", "/quirks/trait", delayedInits))


def _pPerks(cls, delayedInits):
    return map(cls.db.reg, _pTraits(cls, "perks.xml", "/perks/trait", delayedInits))


def _pSpecies(cls, delayedInits=None):
    xml = xmlutils.parseAndValidateXML('species.xml')
    sl = xml.xpath('/species-list/species')
    assert len(sl) > 0

    def resolveTrait(ref_xml, trait_type):
        key = ref_xml.get('ref')
        assert key
        trait = trait_type.db.get(key)
        assert trait, key
        assert trait.name, key
        # print(trait.name)
        return trait

    for xml in sl:
        name = xml.get('name')
        s = Species(parent=g.getApp(), identifier=Id(name))

        def resolveList(modelType, xp):
            l = [resolveTrait(x, modelType) for x in xml.xpath(xp)]
            # for ll in l:
            #    print(ll.value)
            return QQmlListProperty(modelType, s, l)

        s.name = name
        s.cost = int(xml.get('cost'))
        s.baseLE = int(xml.xpath('./point-modifiers/LE-base/@value')[0])
        s.baseSK = int(xml.xpath('./point-modifiers/SK-base/@value')[0])
        s.baseZ = int(xml.xpath('./point-modifiers/Z-base/@value')[0])
        s.baseGS = int(xml.xpath('./point-modifiers/GS-base/@value')[0])
        s.unusualPerkList = resolveList(Perk, './unusual-perks/*')
        s.unusualQuirkList = []  # resolveList(Quirk, './unusual-quirks/*')
        s.perkList = resolveList(Perk, './usual-perks/*')
        s.quirkList = []  # resolveList(Quirk, './usual-quirks/*')

        #TODO
        s.eyeColorList = xml.xpath('./eye_colors/eye_color/@name')
        s.hairColorList = xml.xpath('./hair-colors/hair-color/@name')
        s.weightLimits = xml.xpath('./weight/range/@*')
        s.heightLimits = xml.xpath('./height/range/@*')
        s.talentBoniList = xml.xpath('./talent-bonus/*')
        s.cultureList = xml.xpath('./cultures/*')
        # todo starting ages
        s.assertFrozenAttrs()
        yield s


_dict = {
    Perk: _pPerks,
    Quirk: _pQuirks,
    Species: _pSpecies,
}


def parse(cls, delayedInits=None):
    return _dict[cls](cls, delayedInits)

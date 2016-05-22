import inspect
import logging
import re
import types
from collections import OrderedDict, defaultdict
from copy import copy

from model import *
from relop import RelOp
from xmlutils import parseAndValidateXML

logger = logging.getLogger(__name__)

_usedTypes = [RelOp, Trait]


def isValidPythonIdentifer(text):
    words = re.sub('[^\w]', ' ', text).split()
    return (
        len(words) == 1 and
        len(words[0]) == len(text) and
        len(text) > 0
    )


class ConditionCheck:
    Map = dict()

    @classmethod
    def readAll(cls):
        logger.info("ConditionCheckType.readAll")
        xml = parseAndValidateXML('conditiontypes.xml')
        condTypes = xml.xpath('//condition-type')
        for condType in condTypes:
            condName = condType.get('id')
            argTypes = OrderedDict()
            for arg in condType.xpath('./args/arg'):
                argId = arg.get('id')
                argTypeName = arg.get('type')
                assert isValidPythonIdentifer(argTypeName), 'type "{0}" cannot be a valid python type'.format(
                    argTypeName)
                try:
                    argType = eval(argTypeName)
                except NameError as e:
                    logger.error((
                             'error loading condition "{0}", '
                             'python type "{1}" is not known in conditionchecks.py, missing import?'
                         ).format(condName, argTypeName)
                     )
                    raise e
                assert inspect.isclass(argType)
                argTypes[argId] = argType
            codeText = condType.xpath('./code/text()')[0]
            try:
                code = compile(codeText, '<string>', 'eval')
            except (NameError, TypeError, SyntaxError) as e:
                logger.error('error parsing code for condition "{0}": {1}'.format(condName, e))
                raise e
            cls.Map[condName] = ConditionCheck(condName, argTypes, code, codeText)

    @classmethod
    def get(cls, typeId):
        return cls.Map[typeId]

    def __init__(self, name, argTypes, code, codeText):
        assert isinstance(name, str)
        self.name = name
        self.argTypeMap = argTypes
        assert isinstance(code, types.CodeType)
        self.code = code
        self.codeText = codeText

    def instantiate(self, displayText, **kwargs):
        condChecker = ConditionCheckInstance(self, displayText)
        logger.info("ConditionCheck.instantiate: %s", kwargs)
        for argId, argType in self.argTypeMap.items():
            kwarg = kwargs[argId]
            assert argId in kwargs, "arg '{0}' missing from instantiate".format(argId)
            if not isinstance(kwarg, argType):
                if hasattr(argType, 'fromDB'):
                    argRaw = str(kwarg)
                    kwarg = argType.fromDB(argRaw)
                    if kwarg:
                        logger.info('arg "%s" argType "%s" has fromDB: "%s" -> "%s"', argId, argType.__name__, argRaw,
                                    kwarg)
                    else:
                        logger.error('arg "%s" argType "%s" has fromDB: "%s" -> "%s"', argId, argType.__name__, argRaw,
                                     kwarg)
                else:
                    kwarg = argType(kwarg)
            if not isinstance(kwarg, argType):
                logger.error(
                    'arg "%s" type missmatch: "%s" - "%s"' % (argId, kwarg.__class__.__name__, argType.__name__))
                raise TypeError(
                    'arg "%s" type missmatch: "%s" - "%s"' % (argId, kwarg.__class__.__name__, argType.__name__))
            setattr(condChecker, argId, kwarg)
        me = self

        def Eval(char, args):
            try:
                assert char and args
                return eval(me.code)
            except Exception as e:
                logger.error('condition eval failed: "%s" \n%s', me.codeText, e)
                raise e

        condChecker.eval = (lambda char, args=condChecker: Eval(char, args))
        logger.info('condition "%s" instantiated', me.name)
        return condChecker

    @classmethod
    def xmlParse(cls, xml, logContext="None"):
        constraints = xml.xpath('./constraint')
        for constraint in constraints:
            text = constraint.xpath('./display-text/text()')
            text = text[0] if len(text) else ""
            logger.info("%s: parsing constraint: %s", logContext, text)
            for xcondition in constraint.xpath('./condition'):
                condName = xcondition.get('id')
                if condName in cls.Map:
                    xargs = xcondition.xpath('arg')
                    args = defaultdict(list)
                    for arg in xargs:
                        argId = arg.get('id')
                        argVal = arg.xpath('./text()')[0]
                        args[argId].append(argVal)
                    logger.info("%s: parsing condition %s, args: %s", logContext, condName, args)
                    cc = cls.get(condName)

                    def instantiate(oargs):
                        try:
                            flattened_args = dict()
                            for oargId, argValues in oargs.items():
                                assert len(argValues) == 1
                                flattened_args[oargId] = argValues[0]
                            return cc.instantiate(text, **flattened_args)
                        except Exception as e:
                            logger.error("%s: failed to instantiate condition %s, error: %s", logContext, condName, e)

                    multArgId, multArgList = next(filter(lambda argList: len(argList[1]) > 1, args.items()), None)
                    for multArg in multArgList:
                        multArgs = copy(args)
                        multArgs[multArgId] = [multArg]
                        condition = instantiate(multArgs)
                        if condition:
                            yield condition
                    else:
                        condition = instantiate(args)
                        if condition:
                            yield condition

                else:
                    logger.error('%s: unknown condition type: "%s"', logContext, condName)


class DelayedConditionInstantiation:
    def __init__(self):
        pass


class ConditionCheckInstance:
    def __init__(self, conditionType, text):
        self.conditionType = conditionType
        self.text = text

    def eval(self, char, args):
        pass

    def __str__(self):
        return self.text


ConditionCheck.readAll()

'''
c = ConditionCheckType.get('traitStatusCheck').instantiate(
    traitId=Id(),
    traitStatus=TraitStatusEnum.NORMAL,
    relOp=relop.LessEq
)
char = Character()
print(c.eval(char))
'''

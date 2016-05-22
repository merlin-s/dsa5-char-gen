from globals import xmlRoot
from lxml import etree
from os import path
import logging

logger = logging.getLogger(__name__)


class XmlError(Exception):
    def __init__(self, msg):
        super(XmlError, self).__init__(msg)


def parseAndValidateXML(xmlFileName):
    def xmlAssert(cond, msg):
        if not cond:
            raise XmlError(msg)
    xmlFilePath = path.join(xmlRoot, xmlFileName)
    xmlFile = open(xmlFilePath, 'r')
    logger.info('parsing: %s', xmlFileName)
    assert xmlFile, 'failed to open file'
    xml = etree.parse(xmlFile)
    root = xml.getroot()
    xsdNsAttrs = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
    xsdNsAttrs = [xsd.strip() for xsd in (xsdNsAttrs.split(" ") if xsdNsAttrs else "")]
    xsdAttrs = xsdNsAttrs
    xsdNoNsAttr = root.get('{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation')
    if xsdNoNsAttr:
        xsdAttrs.append(xsdNoNsAttr)
    logger.debug("found following xsd tags: %s", xsdAttrs)
    for xsdAttr in xsdAttrs:
        xsdFilePath = path.join(xmlRoot, xsdAttr)
        with open(xsdFilePath, 'r') as xsdFile:
            xsdXml = etree.parse(xsdFile)
            xmlAssert(xsdXml, 'schema file "%s": invalid XML' % xsdFilePath)
            xsd = etree.XMLSchema(xsdXml)
            xmlAssert(xsd, 'schema file "%s": invalid XSD' % xsdFilePath)
            xmlAssert(xsd.validate(root), 'xml %s invalid: \n%s' % (xmlFileName, xsd.error_log))
            logger.info('%s validated against schema: %s',  xmlFileName, xsdAttr)
    if len(xsdAttrs) == 0:
        logger.warn("missing xsd attribute: \"%s\"" % xmlFileName)
    return xml
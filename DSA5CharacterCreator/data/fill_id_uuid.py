#! /usr/bin/python

import uuid
import lxml
import sys
import os
from lxml import etree
from io import StringIO, BytesIO

filename = sys.argv[1]

with open(filename,'r') as f:
    tree = etree.parse(f)
    root = tree.getroot()

idnodes= root.xpath("//*[@id]")
for node in idnodes:
    id = node.get("id")
    if id and len(id) == 0:
        node.set("id", "%s" % uuid.uuid4())

newtext=etree.tostring(root, pretty_print=True, xml_declaration=True)

with open(filename,'w') as f:
    f.write(newtext)

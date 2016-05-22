# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

import globals
import rc

import model as MODEL
import model.parsers as modelParsers
import character

Character = character.Character

assert rc
#import ctypes
#ctypes.CDLL(ctypes.util.find_library('GL'), ctypes.RTLD_GLOBAL)

logger = logging.getLogger(__name__)


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        stderrHandler = logging.StreamHandler(stream=sys.stderr)
        stderrHandler.setLevel(logging.WARN)
        stdoutHandler = logging.StreamHandler(stream=sys.stdout)
        stdoutHandler.setLevel(logging.INFO)
        stdoutHandler.filter = lambda rec: rec.levelno <= stdoutHandler.level
        logging.basicConfig(
            format='%(name)-15s %(message)s',
            level=logging.INFO,
            handlers=[stderrHandler, stdoutHandler]
        )
        logger.info("__init__")
        self._qml_engine = QQmlApplicationEngine()
        self._root_context = self._qml_engine.rootContext()
        self.char = Character(self)

    def setContext(self, name, value):
        self._root_context.setContextProperty(name, value)

    def start(self):
        logger.info("start")
        self.setContext('character', self.char)
        self.readModels()
        self._qml_engine.load(QUrl("qrc:/ui/main.qml"))

    def readModels(self):
        logger.info("readModels")
        modelTypes = [
            MODEL.Perk,
            MODEL.Quirk,
            MODEL.Species
        ]
        allDelayedInits = {}
        for modelType in modelTypes:
            delayedInits = []
            logger.info("parsing model %s", modelType.__name__)
            g = modelParsers.parse(modelType, delayedInits=delayedInits)
            allDelayedInits[modelType] = delayedInits
            model = list(g)
            # TODO
            name = "%sModel" % modelType.__name__
            assert model is not None, "failed to parse {0}".format(modelType.__name__)
            self.setContext(name, model)
        for modelType, delayedInits in allDelayedInits.items():
            logger.info("delayed init model %s (%s)", modelType.__name__, len(delayedInits))
            for delayedInit in delayedInits:
                delayedInit()

    def exec(self):
        logger.info("exec")
        super().exec()

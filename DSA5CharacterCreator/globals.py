import os
app_dir = os.path.dirname(os.path.realpath(__file__))
xmlRoot = os.path.join(app_dir, 'data')
_app = None


def setApp(app):
    global _app
    _app = app


def getApp():
    return _app

#!env python3
# -*- coding: utf-8 -*-

import sys
import globals as g
import application as app

try:
    # handle ctrl+c on Linux
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    signal = None
    pass

if __name__ == '__main__':
    app = app.Application(sys.argv)
    g.setApp(app)
    app.start()
    app.exec()

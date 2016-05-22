pragma Singleton
import QtQuick 2.2
import 'util.js' as Util

QtObject {
    property QtObject base: QtObject {
        id: b
        property color fgi: "#000"
        property color fga: "#fff"

        property color bga: "#0f0"
    }
    property color bg0:           "#000"
    property color bg1:           "#111"
    property color bg2:           "#222"

    property color bg0a:          Util.tint(bg0, b.bga, 0.3)
    property color bg1a:          Util.tint(bg1, b.bga, 0.3)
    property color bg2a:          Util.tint(bg2, b.bga, 0.3)

    //property color bg0a:

    property color highlight:       Qt.rgba(.10, 1.0, .10)
    property color shadow:          Qt.rgba(.10, .10, .10)


    property QtObject text: QtObject {
        property color normal:   "#aaa"
        property color inactive: "#888"
        property color active:   "#fff"
    }
}
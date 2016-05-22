import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import "."

TabView {
    style: TabViewStyle {
        frameOverlap: 1
        frame: Rectangle {
            color: Palette.bg1
        }
        tabBar: Rectangle {
            color: Palette.bg0
        }
        tab: Rectangle {
            color: styleData.selected ? Palette.bg1  : Palette.bg1a
            border.color:  Palette.bg1
            implicitWidth: Math.max(text.width + 4, 80)
            implicitHeight: 30
            radius: 2
            SText {
                id: text
                anchors.centerIn: parent
                text: styleData.title
                highlight: !styleData.selected
            }
        }
    }
}
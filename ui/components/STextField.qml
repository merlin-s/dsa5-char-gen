import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import "."

TextField {
    style: TextFieldStyle {
        textColor: Palette.text.normal
        background: Rectangle {
            radius: 2
            implicitWidth: 100
            implicitHeight: 24
            color: Palette.bg2
            border.color: Palette.text.inactive
            border.width: 1
        }
    }
}
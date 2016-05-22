import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import "."

Text {
    property bool highlight: false
    color: highlight ? Palette.text.active : Palette.text.normal
}
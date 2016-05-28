import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1
import 'util.js' as Util
import "."
import "components"

Item {
    /*
    GridLayout{
        anchors.fill: parent
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        anchors.leftMargin: parent.width / 6
        anchors.rightMargin: parent.width / 6
        columns: 2
        columnSpacing: 20
        rowSpacing: 20

        SLabel {
            Layout.columnSpan: 2
            Layout.alignment: Qt.AlignCenter
            text: "Charakterdaten"
            font.pixelSize: 22
        }

        SLabel {
            text: "Name"
            horizontalAlignment: Text.AlignRight
            Layout.fillWidth: true
        }
        STextField {
            Layout.fillWidth: true
            text: character.name
            onEditingFinished: {
                character.name = text
            }
        }

        SLabel {
            text: "Basis AP"
            horizontalAlignment: Text.AlignRight
            Layout.fillWidth: true
        }
        STextField {
            Layout.fillWidth: true
            text: character.ap
            onEditingFinished: {
                character.ap = text
            }
            validator: IntValidator {}
        }

        Item {
            Layout.columnSpan: 2
            Layout.fillHeight: true
        }
    }
    */
    ListView {
        anchors.fill: parent
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        anchors.leftMargin: parent.width / 6
        anchors.rightMargin: parent.width / 6
        Layout.minimumWidth: 400
        delegate: Item {
            id: item
            height: 50
            width: parent.width * 0.66
            RowLayout {
                anchors.fill: parent
                Item { Layout.fillWidth: true }
                SLabel {
                    text: modelData.name
                }
                STextField {
                    Layout.preferredWidth: 150
                    Layout.maximumWidth: 300
                    text: modelData.value
                    onEditingFinished: {
                        modelData.value = text
                    }
                    //validator: IntValidator {}
                }
            }
        }
        model: character.appearance
    }
}

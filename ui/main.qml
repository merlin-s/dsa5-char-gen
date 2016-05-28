import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import "."
import "components"

ApplicationWindow {
    visible: true
    width: 800
    minimumWidth: 500
    height: 600
    title: qsTr("DSA5CharacterCreator")
    /*
    style: ApplicationWindowStyle {
        background: Rectangle {
            color: Palette.background
        }
    }
    menuBar: MenuBar {

        style: MenuBarStyle {
            background: Rectangle {
                color: Palette.background
            }
        }
        Menu {
            title: qsTr("Datei")
            MenuItem {
                text: qsTr("Speichern")
                //shortcut: StandardKey.Save
                onTriggered: console.log(text);
            }
            MenuItem {
                text: qsTr("Drucken")
                //shortcut: StandardKey.Print
                onTriggered: console.log(text);
            }
            MenuItem {
                text: qsTr("Verlassen")
                //shortcut: StandardKey.Quit
                onTriggered: Qt.quit();
            }
        }
    }
    */
    SplitView {
        anchors.fill: parent
        STabView {
            Layout.fillWidth: true
            Tab {
                title: "Basisdaten"
                TabWelcome {}
            }
            Tab {
                title: "Rasse"
                TabSpecies {}
            }
            Tab {
                title: "Aussehen"
                TabAppearance {}
            }
            Tab {
                title: "Vorteile"
                TabTraits {
                    model: PerkModel
                }
            }
            Tab {
                title: "Nachteile"
                TabTraits {
                    model: QuirkModel
                }
            }
        }
        Item {
            Layout.minimumWidth: 160
            Layout.maximumWidth: 200
            GridLayout{
                anchors.fill: parent
                anchors.topMargin: 20
                anchors.bottomMargin: 20
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                columns: 2
                columnSpacing: 20
                rowSpacing: 20

                SLabel {
                    Layout.columnSpan: 2
                    Layout.alignment: Qt.AlignLeft
                    text: "Charakterdaten"
                    font.pixelSize: 18
                }

                SLabel {
                    text: "Name"
                    horizontalAlignment: Text.AlignLeft
                    Layout.fillWidth: true
                }
                SLabel {
                    text: character.name
                }

                SLabel {
                    text: "Basis AP"
                    horizontalAlignment: Text.AlignLeft
                    Layout.fillWidth: true
                }
                SLabel {
                    text: character.ap
                }

                Item {
                    Layout.columnSpan: 2
                    Layout.fillHeight: true
                }
            }
        }
    }
}


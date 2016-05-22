import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1
import 'util.js' as Util
import "."
import "components"

Item {
    ListDetailView {
        detailDelegate: Component {
            id: detailComponent
            GridLayout{
                id: me
                property var modelData
                property alias m: me.modelData
                anchors.fill: parent
                columns: 2
                columnSpacing: 20
                rowSpacing: 1

                SLabel {
                    text: m.name
                    Layout.columnSpan: 2
                    Layout.minimumHeight: 40
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                SLabel { text: "AP-Kosten:" }
                SLabel { text: Util.padl('   ', m.cost)+" AP"; font.family: "fixed-width" }

                SLabel {Layout.columnSpan: 2}

                SLabel { text: "Grundwert Lebensenergie (LE):" }
                SLabel { text: Util.padl('   ', m.baseLE); font.family: "fixed-width" }

                SLabel { text: "Grundwert Seelenkraft (SK):" }
                SLabel { text: Util.padl('   ', m.baseSK); font.family: "fixed-width" }

                SLabel { text: "Grundwert Zähigkeit (Z):" }
                SLabel { text: Util.padl('   ', m.baseZ); font.family: "fixed-width" }

                SLabel { text: "Grundwert Geschwindigkeit (GS):" }
                SLabel { text: Util.padl('   ', m.baseGS); font.family: "fixed-width" }

                SLabel {Layout.columnSpan: 2}

                SLabel {
                    Layout.columnSpan: 2
                    Layout.fillHeight: true
                    text: qsTr("Übliche Vorteile:")
                    ListView {
                        anchors.fill: parent
                        anchors.topMargin: 20
                        anchors.leftMargin: 15
                        delegate: Item {
                            height: 15
                            SLabel {
                                text: modelData.name
                                Layout.columnSpan: 2
                                Layout.minimumHeight: 10
                            }
                        }
                        model: m.perkList
                    }
                }
            }
        }

        id: listView1
        anchors.fill: parent
        model: SpeciesModel
        exclusive : true
        descDelegateFunc: function(m) {
            return "%1 AP".arg(m.cost)
        }
    }
}

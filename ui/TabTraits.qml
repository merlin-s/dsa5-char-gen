import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1
import 'util.js' as Util
import "."
import "components"

Item {
    property alias model: ldv.model
    ListDetailView {
    id: ldv
        detailDelegate: Component {
            id: detailComponent
            GridLayout{
                id: me
                property var m
                anchors.fill: parent
                columns: 2
                columnSpacing: 20
                rowSpacing: 1

                SLabel { text: "AP-Kosten:" }
                SLabel { text: Util.padl('   ', m.cost)+" AP"; font.family: "fixed-width" }

                SLabel {}
                SLabel {}

                SLabel { text: "uuid" }
                SLabel { text: Util.padl('   ', m.uuid); font.family: "fixed-width" }

                SLabel { text: "Grundwert Seelenkraft (SK):" }
                SLabel { text: Util.padl('   ', m.baseSK); font.family: "fixed-width" }

                SLabel { text: "Grundwert Zähigkeit (Z):" }
                SLabel { text: Util.padl('   ', m.baseZ); font.family: "fixed-width" }

                SLabel { text: "Grundwert Geschwindigkeit (GS):" }
                SLabel { text: Util.padl('   ', m.baseGS); font.family: "fixed-width" }

                Item {
                    height: 1
                    ListView {
                        anchors.fill: parent
                        delegate: Item {
                            SLabel { text: "X" + modelData.value }
                        }
                        model: m.perkList
                    }
                }
                SLabel { text: 'x' }

                Item { Layout.fillHeight: true }
                Item { Layout.fillHeight: true }
            }
        }
        anchors.fill: parent
        descDelegateFunc: function(m) {
            return "%1 AP".arg(m.cost)
        }
    }
}

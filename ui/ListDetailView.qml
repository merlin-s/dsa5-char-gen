import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import 'util.js' as Util
import "."
import "components"

Item {
    property alias model: listView.model
    property var descDelegateFunc
    property var detailDelegate
    property bool exclusive
    property var onSelectionChanged

    id: root

    SplitView {
        anchors.rightMargin: 15
        anchors.leftMargin: 15
        anchors.bottomMargin: 15
        anchors.topMargin: 15
        anchors.fill: parent
        ScrollView {
            id: scrollView
            Layout.maximumWidth: parent.width * 0.8
            Layout.preferredWidth: parent.width * 0.4
            width: parent.width * 0.4
            Layout.fillHeight: true
            ListView {
                id: listView
                anchors.fill: parent
                Layout.fillHeight: true
                ExclusiveGroup {
                    id: selectorGroup
                }
                function recurse(current, depth, maxDepth) {
                    var minWidth = current.Layout.minimumWidth
                    if( minWidth > 0 )
                        return minWidth
                    minWidth = 0
                    for(var i=0; i<current.children.length; ++i) {
                        var child = current.children[i]
                        var minWidthIt = child.Layout.minimumWidth
                        if(!(minWidthIt > 0) && depth < maxDepth) {
                            minWidthIt = recurse(child, depth+1)
                        }
                        if(minWidthIt > 0)
                            minWidth = Math.max(minWidthIt, minWidth)
                    }
                    return minWidth
                }

                function checkMinSize() {
                    var mw = recurse(listView, 0, 1)
                    scrollView.Layout.minimumWidth = mw
                }

                Component.onCompleted: {
                    checkMinSize()
                }

                delegate: Item {
                    height: 34
                    width: parent.width
                    Layout.minimumWidth: nameText.width + detailText.width + 60 // margins
                    MouseArea {
                        anchors.fill: parent
                        anchors.rightMargin: 15
                        anchors.leftMargin: 15
                        anchors.bottomMargin: 1
                        anchors.topMargin: 1
                        height: parent.height - (anchors.bottomMargin + anchors.topMargin)
                        hoverEnabled: true
                        Rectangle {
                            anchors.fill: parent
                            color: selector.checked
                                    ? Palette.bg2
                                    : Palette.bg0
                            Action {
                                id: selector
                                checkable: true
                                exclusiveGroup: root.exclusive ? selectorGroup : null
                                onToggled: {
                                    root.onSelectionChanged(modelData, checked)
                                }
                                function toggle() {
                                    checked = !checked
                                }
                            }
                            Rectangle {
                                anchors.left: parent.left
                                anchors.top: parent.top
                                anchors.topMargin: (parent.height - height)/2
                                anchors.leftMargin: 5
                                height: parent.height / 5
                                width: height
                                color: selector.checked ? Palette.bg2a : Palette.bg0
                            }
                            SText {
                                id: nameText
                                anchors.top: parent.top
                                anchors.left: parent.left
                                verticalAlignment: Text.AlignVCenter
                                anchors.leftMargin: 17
                                height: parent.height
                                text: '%1'.arg(modelData.name)
                                highlight: selector.checked
                            }
                            SText {
                                id: detailText
                                horizontalAlignment: Text.AlignRight
                                verticalAlignment: Text.AlignVCenter
                                anchors.top: parent.top
                                anchors.right: parent.right
                                anchors.rightMargin: 5
                                height: parent.height
                                text: descDelegateFunc(modelData)
                                highlight: selector.checked
                            }
                        }
                        function loadDetailItem() {
                            var detailItem = detailContainer.children[0]
                            if( typeof detailItem != "undefined") {
                                detailItem.m = modelData
                            } else {
                                if( detailDelegate.status == Component.Error) {
                                    console.warn(detailDelegate.errorString());
                                }
                                var obj = detailDelegate.createObject(detailContainer, {"m":modelData})
                                if (obj == null) {
                                    console.warn("failed to create detailDelegate");
                                }
                            }
                        }
                        onEntered: {
                            loadDetailItem()
                        }
                        onExited: {}
                        onClicked: {
                            selector.toggle()
                        }
                        Component.onCompleted: {
                            loadDetailItem()
                            listView.checkMinSize()
                        }
                    } // MouseArea
                } // delegate
            } // ListView
        } // ScrollView
        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: 100
            Layout.maximumWidth: parent.width * 0.8
            Layout.preferredWidth: parent.width * 0.5
            Item {
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                id: detailContainer
            }
        }
    }

    exclusive: false
    onSelectionChanged: function(current, selected) {
        character.onSelectionChanged(current, selected)
    }
}
/**/
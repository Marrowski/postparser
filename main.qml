import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window
    title: qsTr("Парсер для пошти України")
    width: 1000
    height: 800
    color: "gray"
    visible: true

    Column {
        spacing: 10
        anchors.centerIn: parent

        Text {
            text: "Парсер поштових сервісів України"
            font.family: "Sans Regular"
            font.pointSize: 40
            color: "#20b9f3"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ComboBox {
            id: comboboxPost
            width: 300
            model: ["Нова пошта трекінг", "Нова Пошта відділення"]

            onCurrentTextChanged: {
                if (currentText === "Нова пошта трекінг") {
                    cityInput.placeholderText = "Введіть трек-номер (14 цифр)"
                } else if (currentText === "Нова Пошта відділення") {
                    cityInput.placeholderText = "Введіть назву міста"
                }
            }
        }

        TextField {
            id: cityInput
            width: 300
            height: 40
            font.pixelSize: 18
            placeholderText: "Введіть дані..."
            onTextChanged: mainApp.set_user_input(text)
        }

        Button {
            id: findButton
            text: "Знайти"
            onClicked: {
                if (comboboxPost.currentText === "Нова пошта трекінг") {
                    mainApp.get_tracking()
                } else if (comboboxPost.currentText === "Нова Пошта відділення") {
                    mainApp.get_data()
                }
            }
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ScrollView {
            width: 700
            height: 300
            anchors.horizontalCenter: parent.horizontalCenter

            ListView {
                id: cityOutput
                model: mainApp.response_list

                delegate: Item {
                    width: cityOutput.width
                    height: 80

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "white"
                        radius: 5
                        border.color: "black"

                        Text {
                            text: modelData
                            wrapMode: Text.WordWrap
                            font.pixelSize: 14
                            anchors.fill: parent
                            anchors.margins: 5
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: mainApp
        onData_upd: cityOutput.model = mainApp.response_list
    }
}

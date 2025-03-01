import QtQuick
import QtQuick.Controls

ApplicationWindow 
{
    id: window
    title: qsTr("Парсер для пошти України")
    width: 1000
    height: 800
    color: "gray"
    visible: true

    Text {
        text: "Парсер поштових сервісів України"
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: "Sans Regular"
        font.pointSize: 40
        color: "#20b9f3"
    }

    ComboBox{
        id:comboboxPost
        height: 40
        width: 500
        anchors.centerIn: parent
        model: ["Укрпошта", "Нова Пошта", "Meest Express"]

        background: Rectangle{
            color: comboboxPost.currentText === "Укрпошта" ? "yellow":
            comboboxPost.currentText === "Нова Пошта" ? "red":
            comboboxPost.currentText === "Meest Express" ? "blue": "white"
            radius: 5
        }
    }
    TextField{
        id: cityInput
        placeholderText: "Введіть ваше місто..."
        onTextChanged: mainApp.set_user_input(text)
        width: 500
        height: 100
        font.pixelSize: 21
        anchors.horizontalCenter: comboboxPost.horizontalCenter
        anchors.top: comboboxPost.bottom
        anchors.topMargin:5
    }
    Button{
        id: findButton
        text: "Знайти"
        onClicked: mainApp.get_data()
        anchors.horizontalCenter: cityInput.horizontalCenter
        anchors.top: cityInput.bottom
        anchors.topMargin: 10
    }

    ScrollView {
    width: 700
    height: 300
    anchors.horizontalCenter: findButton.horizontalCenter
    anchors.top: findButton.bottom
    anchors.topMargin: 10

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


    Connections {
        target: mainApp
        onData_upd: cityOutput.text = mainApp.response_text
    }
}
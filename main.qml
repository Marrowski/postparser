import QtQuick
import QtQuick.Controls

ApplicationWindow 
{
    id: window
    title: qsTr("Парсер для пошти України")
    width: 1000
    height: 500
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
        width: 500
        height: 100
        font.pixelSize: 21
        anchors.horizontalCenter: comboboxPost.horizontalCenter
        anchors.top: comboboxPost.bottom
        anchors.topMargin:5
    }
    Button{
        text: "Знайти"
        on_clicked: mainApp.get_data()
        anchors.horizontalCenter: cityInput.horizontalCenter
        anchors.top: cityInput.bottom
        anchors.topMargin: 10
    }
}
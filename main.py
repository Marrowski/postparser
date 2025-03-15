import sys
import os
import requests
from PyQt6.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from dotenv import load_dotenv

load_dotenv()
api = os.getenv('API_KEY')

class MainApplication(QObject):
    data_upd = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._user_input = ""
        self._response_list = []

    @pyqtProperty("QVariantList", notify=data_upd)
    def response_list(self):
        return self._response_list

    @pyqtSlot(str)
    def set_user_input(self, value):
        self._user_input = value.strip()

    @pyqtSlot()
    def get_data(self):
        if not self._user_input:
            self._response_list = ["Будь ласка, введіть ваше місто!"]
            self.data_upd.emit()
            return
        
        try:
            url = 'https://api.novaposhta.ua/v2.0/json/'
            data = {
                "apiKey": api,
                "modelName": "Address",
                "calledMethod": "getWarehouses",
                "methodProperties": {"CityName": self._user_input}
            }
            response = requests.post(url, json=data)
            response_data = response.json()

            self._response_list = [
                f"Тип: {item['Description']}\nАдреса: {item['ShortAddress']}\nНомер відділення: {item['Number']}"
                for item in response_data.get("data", [])
            ] or ["Не знайдено відділень за вашим запитом."]

        except requests.RequestException as e:
            self._response_list = [f'Помилка у знаходжені міста: {e}']

        self.data_upd.emit()

    @pyqtSlot()
    def get_tracking(self):
        if not self._user_input:
            self._response_list = ["Будь ласка, введіть номер ТТН!"]
            self.data_upd.emit()
            return
        
        try:
            url = 'https://api.novaposhta.ua/v2.0/json/'
            data = {
                "apiKey": api,
                "modelName": "TrackingDocument",
                "calledMethod": "getStatusDocuments",
                "methodProperties": {
                    'Documents': [{"DocumentNumber": self._user_input}]
                }
            }
            response = requests.post(url, json=data)
            response_data = response.json()

            self._response_list = [
                f"Статус: {item['Status']} ({item['WarehouseRecipient']})"
                for item in response_data.get("data", [])
            ] or ["Не знайдено інформації про відправлення."]

        except requests.RequestException as e:
            self._response_list = [f'Помилка у знаходжені даних: {e}']

        self.data_upd.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApplication()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("mainApp", mainApp)
    engine.load(os.path.join(os.path.dirname(__file__), 'main.qml'))
    sys.exit(app.exec())

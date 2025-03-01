import sys
import os
from PyQt6.QtCore import QUrl, QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6 import QtCore, QtGui

from dotenv import load_dotenv

import requests

api = os.getenv('API_KEY')


class MainApplication(QObject):
    data_upd = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._city_input = ""
        self._response_text = 'Введіть ваше місто...'
        self._response_data = {}        
        
        
    @pyqtProperty(str, notify=data_upd)
    def response_text(self):
        return self._response_text
    
    
    @pyqtSlot(str)
    def set_user_input(self, value):
        self._city_input = value
    
    
    @pyqtSlot() 
    def get_data(self):
        if not self._city_input.strip():
            self._response_text = 'Будь ласка, введіть ваше місто!'
            self.data_upd.emit()
            return
        try:
            url = 'https://api.novaposhta.ua/v2.0/json/'
            data = {
            "apiKey": api,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityName" : self._city_input,
            }
            }
            response = requests.post(url, json=data)
            self._response_data = response.json()
            
            if "data" in self._response_data and self._response_data['data']:
                results = []
                for data in self._response_data and self._response_data['data']:
                    desc = data['Description']
                    address = data['ShortAddress']
                    number = data['Number']
                    results.append(f'Тип:{desc}\nАдреса:{address}\nНомер відділення:{number}')
                    print(results)
            else:
                self._response_text = 'Не знайдено відділень за вашим запитом.'       
                    
        except requests.RequestException as e:
            self._response_text = f'Помилка у знаходжені міста: {e}'
            
        self.data_upd.emit()
            
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApplication()
    engine = QQmlApplicationEngine()
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    
    context = engine.rootContext()
    context.setContextProperty("mainApp", mainApp)
    
    engine.load(qml_file)
    sys.exit(app.exec())
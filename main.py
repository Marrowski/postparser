import sys
import os
from PyQt6.QtCore import QUrl, QObject, pyqtProperty, pyqtSlot
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6 import QtCore, QtGui

from dotenv import load_dotenv

import requests

api = os.getenv('API_KEY')


class MainApplication(QObject):
    def __init__(self):
        super().__init__()
        self.response_text = 'Очікування відповіді від серверу...'
    
    @pyqtProperty(str)
    def response_text(self):
        return self.response_text
    
    @pyqtSlot()
    def get_data(self):
        try:
            self.response = requests.get('https://api.novaposhta.ua/v2.0/json/')
            return self.response.text
        except requests.exceptions.RequestException:
            return f"Помилка! Код {self.response.status_code}"
        finally:
            return 'Program finished working.'
        
    @pyqtSlot()
    def find_city(self):
        data = {
            "apiKey": api,
            "modelName":"Adress",
            "calledMethod": "searchSettlements",
            "methodProperties":{
                "CityName": input('Введіть ваше місто'),
                "Limit": 5
            }
        }
        
        
        
    response = pyqtProperty(str, get_data)
          


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    
    mainApp = MainApplication()
    context = engine.rootContext()
    context.setContextProperty("mainApp", mainApp)
    
    engine.load(qml_file)
    sys.exit(app.exec())
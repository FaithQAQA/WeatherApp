import sys
import requests
import requests.exceptions
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initIU()

    def initIU(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(500, 600)  # fixed size window for cleaner look
        vbox = QVBoxLayout()
        vbox.setSpacing(20)          # add spacing between widgets
        vbox.setContentsMargins(40, 40, 40, 40)  # padding inside window

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

        # ✨ Jazzed-up stylesheet
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1, 
                stop:0 #89f7fe, stop:1 #66a6ff
            );
        }
        QLabel, QPushButton {
            font-family: 'Segoe UI';
            color: #222;
        }
        QLabel#city_label {
            font-size: 28px;
            font-weight: bold;
            color: white;
        }
        QLineEdit#city_input {
            font-size: 22px;
            padding: 10px;
            border: 2px solid white;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.8);
        }
        QPushButton#get_weather_button {
            font-size: 22px;
            font-weight: bold;
            padding: 12px;
            border-radius: 12px;
            background-color: #4CAF50;
            color: white;
        }
        QPushButton#get_weather_button:hover {
            background-color: #45a049;
        }
        QLabel#temperature_label {
            font-size: 60px;
            font-weight: bold;
            color: white;
        }
        QLabel#emoji_label {
            font-size: 90px;
        }
        QLabel#description_label {
            font-size: 28px;
            color: white;
            font-style: italic;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "d40fa422f555b2ddf2d7c844ca99f63d"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Error retrieving data"))

        except requests.exceptions.RequestException as e:
            self.display_error(str(e))

    def display_error(self, message):
        self.temperature_label.setText("⚠️")
        self.emoji_label.clear()
        self.description_label.setText(message)

    def display_weather(self, data):
        temperature_c = data["main"]["temp"]
        temperature_f = (temperature_c * 9/5) + 32
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.1f}°C / {temperature_f:.1f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

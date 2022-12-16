import sys
import requests
from datetime import datetime

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QDesktopServices


URL_GITHUB_MAIN = "https://github.com/Makusm1990/NENS/raw/main/Final/.exe/"
URL_GITHUB_REPOS = "https://api.github.com/user/repos"

GIT_TOKEN = "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"

headers = {"Authorization": f"Bearer {GIT_TOKEN}"}

response = requests.get(URL_GITHUB_REPOS, headers=headers)
repositories = response.json()

for repository in repositories:
    if repository["full_name"] == "Makusm1990/NENS":
        last_update = repository["pushed_at"]
        update_date = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%SZ")
        formatted_timestamp = update_date.strftime("%d.%B %Y")
        break

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("NENS Update Service")
window.setWindowIcon(QIcon(r"\\dc01\netlogon\Notfall\Logos\logo.png"))
window.resize(400, 200)
screen = QDesktopWidget().screenGeometry()
screen_x = (screen.width() - window.width()) // 2
screen_y = (screen.height() - window.height()) // 2
window.move(screen_x, screen_y)

label = QLabel(f"Last Update: {formatted_timestamp}", window)
label.setAlignment(Qt.AlignCenter)

button_client = QPushButton("Download latest Client version")
button_server = QPushButton("Download latest Server version")

def download_client():
    QDesktopServices.openUrl(QUrl(URL_GITHUB_MAIN + "client_modul.exe"))

def download_server():
    QDesktopServices.openUrl(QUrl(URL_GITHUB_MAIN + "server_receiver.exe"))

button_client.clicked.connect(download_client)
button_server.clicked.connect(download_server)

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button_client)
layout.addWidget(button_server)

window.setLayout(layout)

window.show()
sys.exit(app.exec_())

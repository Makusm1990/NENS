import sys
import os
import pprint
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDesktopWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices

from datetime import datetime


# Erstelle eine QApplication (erforderlich, um eine GUI zu erstellen)
app = QApplication(sys.argv)

# Erstelle das Hauptfenster
window = QWidget()
window.setWindowTitle("NENS Update Service")
# Set the window icon
icon = QIcon(r'\\dc01\netlogon\Notfall\Logos\logo.png')
window.setWindowIcon(icon)
# Set the size and position of the window
window.resize(400, 200)

# Get the screen dimensions
screen = QDesktopWidget().screenGeometry()

# Calculate the center position of the screen
x = (screen.width() - window.width()) // 2
y = (screen.height() - window.height()) // 2

# Move the window to the center of the screen
window.move(x, y)



# Setze den Zugriffstoken in einer Umgebungsvariable
access_token = "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"

# Setze den API-Endpunkt und die Autorisierungsheader
url = "https://api.github.com/user/repos"
headers = {"Authorization": f"Bearer {access_token}"}

# Sende die Anforderung und speichere die Antwort
response = requests.get(url, headers=headers)
repositories = response.json()

# Durchlaufe die Liste der Repositories und drucke den Namen jedes Repositorys aus
for repository in repositories:
    if repository["full_name"] == "Makusm1990/NENS":
        last_update = repository["pushed_at"]

        update_date = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%SZ")
        formatted_timestamp = update_date.strftime("%d.%B %Y, %H:%M Uhr")


# Create the label
label = QLabel(f"Last Update: {str(formatted_timestamp)}", window)

# Set the alignment of the label to center
label.setAlignment(Qt.AlignCenter)

# Create the button
button = QPushButton("Click me")

# Define a function to open the website
def open_website():
    QDesktopServices.openUrl(QUrl("https://github.com/Makusm1990/NENS/tree/main/Final/.exe"))
button.clicked.connect(open_website)

# Create a vertical layout and add the label to it
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

# Set the layout as the main layout for the window
window.setLayout(layout)

# Zeige das Fenster
window.show()

# Starte die GUI-Schleife
sys.exit(app.exec_())

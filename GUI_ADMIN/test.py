import sys
from PyQt5.QtWidgets import QApplication, QLabel
import requests
import json

def get_github_user(username):
    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(api_url)
    if response.status_code == 200:
        user_info = json.loads(response.content.decode('utf-8'))
        return user_info
    else:
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_info = get_github_user('octocat')
    if user_info:
        label = QLabel(f'Username: {user_info["login"]}')
        label.show()
    else:
        label = QLabel('User not found')
        label.show()
    sys.exit(app.exec_())
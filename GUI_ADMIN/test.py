import requests

URL = "https://api.github.com/repos/Makusm1990/NENS/commits"

params = {
    "sha": "HEAD",
}


try:
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            print(commit["commit"]["message"])
        latest_commit = commits[0]
        print(latest_commit["commit"]["message"])
    else:
        print(f"Request failed with status code {response.status_code}")
except requests.RequestException as e:
    print(f"There was an error making the request: {e}")
except ValueError as e:
    print(f"There was an error parsing the response as JSON: {e}")
import requests

def get_repo(owner, repo):
  url = "https://api.github.com/repos/" + owner + "/" + repo + "/commits"
  print(url)
  response = requests.get(url)
  print(response.json())

get_repo("torvalds", "linux")
import os, json

class User:
    def __init__(self):
        try:
            self.username = os.environ["USERNAME"]
            self.secret = os.environ["SECRET"]
        except:
            with open("credential.json", "r") as json_file:
                info = json.load(json_file)
            self.username = info["username"]
            self.secret = info["secret"]

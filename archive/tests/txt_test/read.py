import json

with open("level.txt", "r") as f:
    list = json.load(f)
    print(list["rank"])
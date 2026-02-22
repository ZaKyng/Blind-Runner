import json

with open("txt_test/level.txt", "r") as f:
    list = json.load(f)
    print(list)
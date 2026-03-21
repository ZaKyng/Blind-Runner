import json

try:
    with open("level.txt", "r") as f:
        data = json.load(f)
        data["screen_size"] = (900000)

    with open("level.txt", "w") as f:
        json.dump(data, f)
except:
    with open("level.txt", "w") as f:
        data = {}
        data["screen_size"] = (900000)
        json.dump(data, f)
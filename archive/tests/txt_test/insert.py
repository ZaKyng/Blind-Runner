import json

input = input("Enter something to write to the file: ")

a = {
  "data": input,
  "level": 1,
  "rank": "A"
}

with open("level.txt", "w") as f:
    json.dump(a, f)
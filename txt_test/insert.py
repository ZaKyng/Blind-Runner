import json

input = input("Enter something to write to the file: ")

a = {
  "data": input,
  "level": 1,
  "rank": "A"
}

with open("txt_test/level.txt", "w") as f:
    json.dump(a, f)
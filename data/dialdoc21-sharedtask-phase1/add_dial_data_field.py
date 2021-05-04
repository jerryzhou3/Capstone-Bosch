import sys
import json

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    with open(filename.split(".")[0] + "_formatted.json", "w") as f:
        f.write(json.dumps({"dial_data": data}))

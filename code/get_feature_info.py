from argparse import ArgumentParser
from urllib.request import urlopen
import json

parser = ArgumentParser()
parser.add_argument("--data", help="votemanager csv")

args = parser.parse_args()

with open(args.data, "r") as f:
    lines = f.readlines()
    
    cols = lines[1].split(";") # german csvs^^

    date = "".join(cols[0].split(".")[::-1])
    ags = cols[2]

url = f"https://votemanager.kdo.de/{date}/{ags}/daten/opendata/open_data.json"

with urlopen(url) as response:
    data = json.load(response)
    
parties = data["dateifelder"][0]["parteien"]

dict = {p["feld"]: p["wert"] for p in parties}

with open("features.json", "w") as f:
    json.dump(dict, f, indent=4)
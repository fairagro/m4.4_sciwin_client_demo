from argparse import ArgumentParser
from urllib.request import urlopen
from urllib.parse import urljoin
import json

parser = ArgumentParser()
parser.add_argument("--ags", help="ags of city", default="03101000")
parser.add_argument("--election", help="Election of Choice e.g. Bundestagswahl 2025", default="Bundestagswahl 2025")

args = parser.parse_args()
base_url = f"https://votemanager.kdo.de/{args.ags}"
with urlopen(f"{base_url}/api/termine.json") as response:
    data = json.load(response)

keywords = args.election.split(" ")
election = keywords[0]
year = keywords[1]
election = [item for item in data["termine"] if election in item["name"] and year in item["date"]][0]

url = urljoin(urljoin(base_url, election["url"]), "../daten/opendata/open_data.json")

with urlopen(url) as response:
    data = json.load(response)
    
csv = [item for item in data["csvs"] if "Stadtbezirk" in item["ebene"]][0]
csv_url = urljoin(url, csv["url"])

with urlopen(csv_url) as response:
    print(response.read().decode("utf-8"))
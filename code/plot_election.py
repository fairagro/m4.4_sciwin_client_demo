from argparse import ArgumentParser
import pandas as pd
import json
import re

parser = ArgumentParser()
parser.add_argument("--data", help="votemanager csv")
parser.add_argument("--features", help="json dict")

args = parser.parse_args()

test_has_erststimme = {"Europawahl": False,
                       "Bundestagswahl": True,
                       "Landtagswahl": True}

with open(args.data, "r") as f:
    df = pd.read_csv(f, sep=";", encoding="utf-8")

with open(args.features, "r") as f:
    features = json.load(f)

has_erststimme = test_has_erststimme[df['wahl'].iloc[0]]
city_result = df.sum(axis=0)
sum_col = "F" if has_erststimme else "D"

abbr = {
    "Christlich Demokratische Union": "CDU" ,
    "DIE GRÜNEN": "GRÜNE",
    "Sozialdemokratische Partei Deutschlands": "SPD",
    "Alternative für Deutschland": "AfD",
    "Freie Demokratische Partei": "FDP",
    "DIE LINKE": "LINKE",
    "Sahra Wagenknecht": "BSW",
    "Partei für Arbeit, Rechtsstaat, Tierschutz, Elitenförderung und basisdemokratische Initiative": "PARTEI",
    "Volt": "Volt"
}

col = {
    "CDU": "black",
    "SPD": "red",
    "GRÜNE": "green",
    "AfD": "blue",
    "FDP": "yellow",
    "LINKE": "purple",
    "PARTEI": "darkred",
    "Volt": "darkviolet",
    "BSW": "orange"
}

def shorten(v: str) -> str:
    v_lower = v.lower()
    for key, val in abbr.items():
        if key.lower() in v_lower:
            return val
    return v

# alter features to just get numeric value
features = {sum_col + re.search(r'\d+', k).group(): shorten(v) for k, v in features.items()}  # type: ignore

# replace features in city_result and calculate percentage
city_result = city_result[city_result.index.str.startswith(sum_col)]
city_result = city_result.rename(features)
city_result = city_result.div(city_result[sum_col])

low = city_result[city_result < 0.05]
sum = low.sum()

city_result = city_result[city_result >= 0.05]
city_result.drop(sum_col, inplace=True)
city_result["Sonstige"] = sum

city_result = city_result * 100

colors = [col.get(label, "gray") for label in city_result.index]
ax = city_result.plot(kind="bar", color=colors)

ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.figure.savefig("election.png") # type: ignore
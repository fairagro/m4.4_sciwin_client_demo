import json
import pandas as pd
import plotly.express as px
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--geojson", help="geojson file")
parser.add_argument("--csv", help="csv data to map")
parser.add_argument("--on", help="feature to map on 'name_in_csv:name_in_json'")
parser.add_argument("--feature", help="feature ot plot")
parser.add_argument("--output_name", help="filename without extension")

args = parser.parse_args()
with open(args.geojson) as f:
    data = json.load(f)
    
df = pd.read_csv(args.csv, sep=";")
df["gebiet-nr"] = df["gebiet-name"].apply(lambda x: str(x).split(" ")[0])
df["percentage"] = df[args.feature] / df[args.feature[0]]

on = args.on.split(":")

fig = px.choropleth(df, geojson=data, locations=on[0], featureidkey=f"properties.{on[1]}", projection="mercator", color="percentage", color_continuous_scale="Greens")
fig.update_geos(fitbounds="locations", visible=False)
fig.write_image(f"{args.output_name}.png")
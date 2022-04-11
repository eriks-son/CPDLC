import pandas as pd
import requests


departure = "KEWR"

destination = "KRRR"

requested_altitude = 210

aircraft_type = "JET"

if aircraft_type == "JET":
    opposite_type = "PROP"
else:
    opposite_type = "JET"

headers = {"User-Agent": "Mozilla/5.0"}

url = requests.get(f'https://nyartcc.org/prd/?from={departure}&to={destination}')

table_MN = pd.read_html(url.text)

table = table_MN[0]

prd_route = [0 for x in range(len(table))]

print(table["From"][0])

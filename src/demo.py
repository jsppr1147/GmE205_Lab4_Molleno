import json
from spatial import Parcel

with open("data/parcels_shapely_ready.json", encoding="utf-8") as f:
    records = json.load(f)

sample = Parcel.from_dict(records[0]) #checks first parcel data
print(sample.zone, sample.area_sqm, sample.is_active)
print(sample.bbox())
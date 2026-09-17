import json
from spatial import Parcel
from analysis import (total_active_area, parcels_above_threshold, count_by_zone, development_candidates)

with open("data/parcels_shapely_ready.json", encoding="utf-8") as f:
    records = json.load(f)

sample = Parcel.from_dict(records[0])  # checks first parcel data
#print(sample.zone, sample.area_sqm, sample.is_active)
#print(sample.bbox())

parcels = [Parcel.from_dict(record) for record in records]

# check 1: if zone count sum equal to total parcel count
zone_counts = count_by_zone(parcels)
assert sum(zone_counts.values()) == len(parcels), "Zone counts don't add up to total parcels"
print("Zone counts:", zone_counts)


import json
from spatial import Parcel
from analysis import (total_active_area, parcels_above_threshold, count_by_zone, development_candidates,
                      classify_suitability_grid,count_suitable_cells)

with open("data/parcels_shapely_ready.json", encoding="utf-8") as f:
    records = json.load(f)

sample = Parcel.from_dict(records[0])  # checks first parcel data
#print(sample.zone, sample.area_sqm, sample.is_active)
#print(sample.bbox())
'''
parcels = [Parcel.from_dict(record) for record in records]

# check 1: if zone count sum equal to total parcel count
zone_counts = count_by_zone(parcels)
assert sum(zone_counts.values()) == len(parcels), "Zone counts don't add up to total parcels"
print("Zone counts:", zone_counts)

# --- Check 2 & 3: every candidate is valid, and candidates is subset of parcels ---
MIN_AREA = 5000.0
ALLOWED_ZONES = {"Residential", "Commercial"}
candidates = development_candidates(parcels, MIN_AREA, ALLOWED_ZONES)

for parcel in candidates:
    assert parcel.is_active
    assert parcel.zone in ALLOWED_ZONES
    assert parcel.area_sqm >= MIN_AREA
assert all(parcel in parcels for parcel in candidates), "Candidates must be a subset of parcels"
print(f"{len(candidates)} candidates found, all satisfy the rule")

# --- Check 4: changing min_area changes the result ---
more = development_candidates(parcels, 3000.0, ALLOWED_ZONES)
print(f"With min_area=3000: {len(more)} candidates (was {len(candidates)} at 5000)")

fewer = development_candidates(parcels, 7000.0, ALLOWED_ZONES)
print(f"With min_area=7000: {len(fewer)} candidates (was {len(candidates)} at 5000)")
'''
####-----------RASTER---------------------######
with open("data/suitability_grid.json", encoding="utf-8") as f:
    grid_data = json.load(f)

criteria = grid_data["criteria"]
suitability = classify_suitability_grid(
    grid_data["slope_deg"],
    grid_data["flood_m"],
    max_slope=criteria["max_slope_deg"],
    max_flood=criteria["max_flood_m"],
)
print("Suitability grid:", suitability)
print("Suitable cells:", count_suitable_cells(suitability))
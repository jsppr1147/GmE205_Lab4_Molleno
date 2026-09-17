from shapely.geometry import box
from spatial import SpatialObject, Parcel
import json
from analysis import (development_candidates, intersecting_parcels)

study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)
with open("data/parcels_shapely_ready.json", encoding="utf-8") as f:
    records = json.load(f)
parcels = [Parcel.from_dict(record) for record in records]
MIN_AREA = 5000.0
ALLOWED_ZONES = {"Residential", "Commercial"}


candidates = development_candidates(parcels, min_area=MIN_AREA, allowed_zones=ALLOWED_ZONES)
inside_study_area = intersecting_parcels(candidates, study_area)

print(f"{len(candidates)} development candidates")
print(f"{len(inside_study_area)} of those intersect the study area")
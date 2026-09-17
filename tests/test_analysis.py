import pytest
from shapely.geometry import box
from spatial import SpatialObject, Parcel
from analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)

#Run from a terminal like [pytest -v]
#Also needs a pytest.ini for calling the spatial.py which is outside the src folder

#or a more reasonable thing to do in VS code is to access the Python tests CTRL+SHFT+P, select Python Test, select Pytest, then select the test folder
#doing this should show the green play button near the def function which allows the user to check if the a test is working



def make_parcel(parcel_id, zone, is_active, area_sqm, geom=None):
    #make function for testing this script
    geometry = geom or box(0, 0, 1, 1)
    attributes = {"zone": zone, "is_active": is_active, "area_sqm": area_sqm}
    return Parcel(parcel_id, geometry, attributes)


def test_total_active_area_excludes_inactive():
    parcels = [
        make_parcel(1, "Residential", True, 1000.0),
        make_parcel(2, "Residential", False, 5000.0),  # excluded
        make_parcel(3, "Commercial", True, 2000.0),
    ]
    assert total_active_area(parcels) == 3000.0


def test_parcels_above_threshold_includes_exact_match():
    parcels = [
        make_parcel(1, "Residential", True, 5000.0),  # exactly at threshold
        make_parcel(2, "Residential", True, 4999.0),
    ]
    result = parcels_above_threshold(parcels, 5000.0)
    assert [p.parcel_id for p in result] == [1]


def test_count_by_zone_counts_correctly():
    parcels = [
        make_parcel(1, "Residential", True, 1000.0),
        make_parcel(2, "Residential", True, 1000.0),
        make_parcel(3, "Commercial", True, 1000.0),
    ]
    counts = count_by_zone(parcels)
    assert counts == {"Residential": 2, "Commercial": 1}


def test_development_candidates_rejects_inactive():
    parcels = [make_parcel(1, "Residential", False, 6000.0)]
    result = development_candidates(parcels, min_area=5000.0, allowed_zones={"Residential"})
    assert result == []


def test_development_candidates_rejects_disallowed_zone():
    parcels = [make_parcel(1, "Industrial", True, 6000.0)]
    result = development_candidates(parcels, min_area=5000.0, allowed_zones={"Residential"})
    assert result == []


def test_development_candidates_rejects_too_small():
    parcels = [make_parcel(1, "Residential", True, 1000.0)]
    result = development_candidates(parcels, min_area=5000.0, allowed_zones={"Residential"})
    assert result == []


def test_development_candidates_accepts_valid_parcel():
    parcels = [make_parcel(1, "Residential", True, 6000.0)]
    result = development_candidates(parcels, min_area=5000.0, allowed_zones={"Residential"})
    assert [p.parcel_id for p in result] == [1]


def test_intersecting_parcels_finds_inside_and_excludes_outside():
    study_area = SpatialObject(box(0, 0, 2, 2))
    inside = make_parcel(1, "Residential", True, 1000.0, geom=box(0.5, 0.5, 1.5, 1.5))
    outside = make_parcel(2, "Residential", True, 1000.0, geom=box(10, 10, 11, 11))

    result = intersecting_parcels([inside, outside], study_area)
    assert [p.parcel_id for p in result] == [1]


def test_classify_suitability_grid_handles_1_0_nodata():
    slope = [[5, 20], [None, 10]]
    flood = [[0.1, 0.1], [0.2, 0.9]]
    result = classify_suitability_grid(slope, flood, max_slope=15.0, max_flood=0.5)
    assert result == [
        [1, 0],       # suitable, then slope too high
        [None, 0],    # NoData, then flood too high
    ]


def test_count_suitable_cells_ignores_zero_and_nodata():
    grid = [[1, 0], [None, 1]]
    assert count_suitable_cells(grid) == 2
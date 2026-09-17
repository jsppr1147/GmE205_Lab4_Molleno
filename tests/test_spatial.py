import pytest
from spatial import Parcel

#Run from a terminal like [pytest -v]
#Also needs a pytest.ini for calling the spatial.py which is outside the src folder

#or a more reasonable thing to do in VS code is to access the Python tests CTRL+SHFT+P, select Python Test, select Pytest, then select the test folder
#doing this should show the green play button near the def function which allows the user to check if the a test is working

def make_record(parcel_id=1, zone="Residential", is_active=True, area_sqm=6000.0):
    #function for creating records. usable for checking spatial.py where you need to check if it is working as intended
    return {
        "parcel_id": parcel_id,
        "zone": zone,
        "is_active": is_active,
        "area_sqm": area_sqm,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [121.00, 14.60], [121.01, 14.60],
                [121.01, 14.61], [121.00, 14.61],
                [121.00, 14.60],
            ]],
        },
    }


def test_from_dict_sets_expected_fields():
    #create record random -> create parcel 
    #then assert parcel_id, zone, is_active, area_sqm, and geom_type
    record = make_record(parcel_id=7, zone="Commercial", is_active=False, area_sqm=4321.5)
    parcel = Parcel.from_dict(record)

    assert parcel.parcel_id == 7
    assert parcel.zone == "Commercial"
    assert parcel.is_active is False
    assert parcel.area_sqm == 4321.5
    assert parcel.geometry.geom_type == "Polygon"


def test_from_dict_bbox_matches_geometry():
    #create parcel to make record
    #test bbox() method
    parcel = Parcel.from_dict(make_record())
    minx, miny, maxx, maxy = parcel.bbox()
    assert minx == pytest.approx(121.00)
    assert maxx == pytest.approx(121.01)
import math
import csv #for csv reading
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import shape

class SpatialObject:
    ''' Base abstraction for domain objects that have geometry'''
    def __init__(self, geometry):
        self.geometry = geometry

    def bbox(self):
        ''' Return the bounding box of the geometry as a tuple (minx, miny, maxx, maxy)'''
        return self.geometry.bounds

    def intersects(self, other):
        ''' Return True if this object's geometry intersects with another SpatialObject's geometry'''
        return self.geometry.intersects(other.geometry)

class Point(SpatialObject):
    def __init__(self, id, lon, lat, name=None, tag=None):
        # Validate the longitude and latitude values
        # Note that validation must happen before assigning the values to the instance variables
        if not (180.0 >= lon >= -180.0):
            raise ValueError("Longitude must be between -180 and 180 degrees.")
        if not (90.0 >= lat >= -90.0):
            raise ValueError("Latitude must be between -90 and 90 degrees.")

        geometry = ShapelyPoint(lon, lat)  # Create a Shapely Point object for the geometry
        super().__init__(geometry)  # Initialize the base class with the geometry
        self.id = id
        self.name = name
        self.tag = tag

    @property
    def lon(self):
        return self.geometry.x

    @property
    def lat(self):
        return self.geometry.y

    def to_tuple(self) -> tuple[float, float]:
        """
        Return the coordinate as a (lon, lat) tuple.
        """
        return (self.lon, self.lat)

    @classmethod
    def from_dict(cls, d:dict):
        """
        Create a Point object from a dictionary. 
        The dictionary must contain 'id', 'lon', and 'lat' keys. Other keys are optional.
        Relies on the __init__ method to validate the coordinates.
        """
        return cls(
            id=d["id"],
            lon=d["lon"],
            lat=d["lat"],
            name=d.get("name"),
            tag=d.get("tag")
        )       

    def as_dict(self) -> dict:
        """
        Return the Point as a dictionary. 
        Describe point using the primitives, this is useful for serialization (e.g., to JSON).

        Note: self.geometry.bounds returns a tuple of (minx, miny, maxx, maxy), which is the bounding box of the point. 
        self.geometry.bounds is kinda similar to the bbox of a PointSet, but for a single point, the min and max coordinates are the same.
        Note: self.geometry.bounds is a tuple, so we use list(..) to convert it to a list, which is more JSON-friendly.
        """
        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag,
            "geometry": [self.lon, self.lat],
            "bbox": list(self.geometry.bounds)
        }

    
    @staticmethod #a decorator to indicate that this method does not depend on the instance of the class
    def haversine_m(lon1:float, lat1:float, lon2:float, lat2:float)-> float:
        """
        Calculate the haversine distance between two points on the earth
        specified in decimal degrees.
        Returns the distance in meters.
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Radius of earth in meters
        r = 6371000.0
        
        return c * r

    def distance_to(self, other):
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)

    @classmethod
    def from_row(cls,row):
        '''
        Create a Point object from a row of data.'''
        return cls(id=str(row["id"]), 
                   lon=float(row["lon"]),
                   lat=float(row["lat"]),
                   name=row.get("name"),
                   tag=row.get("tag")
                   )
    def is_poi(self):
        return (self.tag or "").lower() == "poi"

class PointSet:

    def __init__(self, points=None):
        #Store the points in a list. If no points are provided, initialize an empty list.
        self.points = list(points) if points is not None else []

    @classmethod
    def from_csv(cls, path: str):
        #Read points from a CSV file and return a Pointset object.
        points = []
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Delegate validation and object creation directly to Point.from_row
                    point = Point.from_row(row)
                    points.append(point)
                except (ValueError, KeyError, TypeError) as exc:
                    # Gracefully skip rows with invalid data/coordinates or missing keys
                    print(f"Skipping invalid row {row}: {exc}")
                    continue
        return cls(points)

    def count(self)-> int:
        #Return the number of points in the Pointset.
        return len(self.points)

    def bbox(self)-> tuple[float, float, float, float]:
        
        #Calculate the bounding box of the points in the Pointset.
        #Returns a tuple of (min_lon, min_lat, max_lon, max_lat).
        if not self.points:
            raise ValueError("Pointset is empty. Cannot calculate bounding box.")
        
        min_lon = min(point.lon for point in self.points)
        max_lon = max(point.lon for point in self.points)
        min_lat = min(point.lat for point in self.points)
        max_lat = max(point.lat for point in self.points)
        
        return (min_lon, min_lat, max_lon, max_lat)

    def filter_by_tag(self, tag: str):
     
        #Filter points by a specific tag.
        #Returns a new Pointset containing only the points with the specified tag.
        
        filtered_points = [point for point in self.points if (point.tag or "").lower() == tag.lower()]
        return PointSet(filtered_points)

class Parcel(SpatialObject):
    def __init__(self, parcel_id, geometry, attributes: dict):
        ''' 
        Represents a land parcel with a unique identifier, geometry, and additional attributes.
        Note: This uses a dictionary for parcel attributes 
        '''
        super().__init__(geometry)
        self.parcel_id = parcel_id
        self.attributes = attributes

    #read only properties
    @property
    def area_sqm(self):
        return float(self.attributes["area_sqm"])

    @property
    def zone(self):
        return self.attributes["zone"]

    @property
    def is_active(self):
        return bool(self.attributes["is_active"])

    @classmethod #allows u to simply call the attributes like object.zone, object.area_sqm from dictionary
    def from_dict(cls, record: dict):
        geometry = shape(record["geometry"])
        attributes = {
            "zone":record["zone"],
            "area_sqm": record["area_sqm"],
            "is_active": record["is_active"],
        }
        return cls(record["parcel_id"], geometry, attributes)
    def as_dict(self) -> dict:
        '''
        Describes the parcel using the primitives, this is useful for serialization (e.g., to JSON).
        Doesnt return the geometry as a shapely object, but rather as a list of coordinates (lon, lat) for each vertex.        
        '''
        return {
            "parcel_id": self.parcel_id,
            "bbox": list(self.bbox()),
            "attributes": self.attributes,
        }
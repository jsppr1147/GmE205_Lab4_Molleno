GmE 205 Lab 4: Spatial Algorithms and Structured Programming  
--------------------------------------------------------------
This laboratory focuses on the expression of familiar operations as algorithms and implement those algorithms using structured programming while maintaining the object-oriented responsibilities established in Lab 3. This laboratory has PARTS A-K, with part A being the setup of files and environment, Part B-H for the exercise, Part I for testing, Part J for the challenges and Part K for the Reflections and Summary. 

--------------------------------------------------------------
PART A. Project Setup and Reproducible Workspace  
- The folder structure recommended for this exercise was created.  
- Similar contents for the .gitignore were placed while minor modifications were placed in the requirements.txt as only matplotlib and shapely are the only requirements for this exercise.
- Python interpreter for the environment was selected to avoid issues.
- Github repository was created and initialized. 
- First commit and push milestone.

Part B. Carry Forward the Laboratory 3 Object Model  
- Inspection of the data input from the data sources like record structure to get a gist of how to import it. 
- Noting to use the area_sqm in the json file instead of computing again from the coordinates boundaries. 
- The parcel access are made accessible by using a @property method so you can write it like parcel.zone instead of parcel.attributes["zones"]. This is so its cleaner in the interface and it avoid the fragile format of parcel.attributes["zones"] which can be prone to missing key or wrong type.
- Added the from_dict to convert the json into a geometry which shapely.geometry.polygon can work on and to reshape these flat records into the attributes the class Parcel expects.
- Added also a demo to check if the property method and the inherited behaviors work fine.

-----------------------------------------------------------------------------------------
PART C. Algorithm First: Expose the GIS Logic   

C1. Analysis Questions:
QUESTION 1:  What is the total area in square meters of all active parcels?

SET total_area = 0
FOR each parcel in parcels
    IF parcel is active
        ADD parcel area_sqm to total_area
    END IF
END FOR    
RETURN total_area

QUESTION 2: Which parcels have area >= threshold?

SET result = empty list
FOR each parcel in parcels
    IF parcel.area_sqm >= threshold
        ADD parcel to result
    END IF
END FOR    
RETURN result

QUESTION 3: How many parcels per zone?

SET counts = empty dictionary
FOR each parcel in parcels
    IF parcel.zone not in counts
        SET counts[parcel.zone] = 0
    END IF
    ADD 1 to counts[parcel.zone] 
ENDFOR
RETURN counts

QUESTION 4: Which parcels are development candidates?

SET result = empty list
FOR each parcel in parcels
    IF parcel.is_active AND parcel.zone in allowed_zones AND parcel.area_sqm >= min_area
        ADD parcel to result
    END IF
END FOR    
RETURN result

QUESTION 5: Which parcels intersect the study area?

SET result = empty list
FOR each parcel in parcels
    IF parcel.intersects(study_area)
        ADD parcel to result
    END IF
END FOR    
RETURN result
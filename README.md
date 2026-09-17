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
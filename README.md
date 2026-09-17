GmE 205 Lab 4: Spatial Algorithms and Structured Programming  
--------------------------------------------------------------
This laboratory focuses on the expression of familiar operations as algorithms and implement those algorithms using structured programming while maintaining the object-oriented responsibilities established in Lab 3. This laboratory has PARTS A-K, with part A being the setup of files and environment, Part B-H for the exercise, Part I for testing, Part J for the challenges and Part K for the Reflections and Summary. 
--------------------------------------------------------------
## Setup and Run Instructions
1. Clone the repository and `cd` into the project root.
2. Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate     
3. Install dependencies:
   pip install -r requirements.txt
4. Run the test suite:
   pytest -v
5. Run the full workflow (must be run from the project root, since data paths are relative):
   python src/run_lab4.py
6. Outputs are written to output/lab4_report.json, output/lab4_vector_preview.png,
   and output/lab4_raster_preview.png.
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

Sequence: runs during the "analyze" step, after parcels are loaded and constructed.
Selection: IF parcel.is_active — decides whether a parcel's area counts.
Repetition: FOR each parcel in parcels — visits every parcel exactly once.
Input: list of Parcel.
Output: float.

QUESTION 2: Which parcels have area >= threshold?  

SET result = empty list  
FOR each parcel in parcels  
    IF parcel.area_sqm >= threshold  
        ADD parcel to result  
    END IF  
END FOR        
RETURN result  

Sequence: runs during the "analyze" step, after parcels are loaded and constructed.
Selection: IF parcel.area_sqm >= threshold — decides whether a parcel is kept.
Repetition: FOR each parcel in parcels — visits every parcel exactly once.
Input: list of Parcel, threshold (float).
Output: list[Parcel].

QUESTION 3: How many parcels per zone?  

SET counts = empty dictionary  
FOR each parcel in parcels  
    IF parcel.zone not in counts  
        SET counts[parcel.zone] = 0  
    END IF  
    ADD 1 to counts[parcel.zone]  
ENDFOR  
RETURN counts  

Sequence: runs during the "analyze" step, after parcels are loaded and constructed.
Selection: IF parcel.zone not in counts — decides whether a new zone key needs initializing.
Repetition: FOR each parcel in parcels — visits every parcel exactly once.
Input: list of Parcel.
Output: dict (zone name -> count).

QUESTION 4: Which parcels are development candidates?  

SET result = empty list  
FOR each parcel in parcels  
    IF parcel.is_active AND parcel.zone in allowed_zones AND parcel.area_sqm >= min_area  
        ADD parcel to result  
    END IF  
END FOR       
RETURN result  

Sequence: runs during the "analyze" step, after parcels are loaded and constructed.
Selection: IF parcel.is_active AND parcel.zone in allowed_zones AND parcel.area_sqm >= min_area — decides whether a parcel qualifies.
Repetition: FOR each parcel in parcels — visits every parcel exactly once.
Input: list of Parcel, min_area (float), allowed_zones (list of str).
Output: list[Parcel].

QUESTION 5: Which parcels intersect the study area?  

SET result = empty list  
FOR each parcel in parcels  
    IF parcel.intersects(study_area)  
        ADD parcel to result  
    END IF  
END FOR      
RETURN result  

Sequence: runs during the "analyze" step, after parcels are loaded and constructed.
Selection: IF parcel.intersects(study_area) — decides whether a parcel spatially overlaps the study area.
Repetition: FOR each parcel in parcels — visits every parcel exactly once.
Input: list of Parcel, study_area (SpatialObject).
Output: list[Parcel].


----------------------------------------------------------------------------------------------
Part D: Structured Vector Analysis
- created the five required functions: total_active_area, parcels_above_threshold, count_by_zone, development_candidates, intersecting_parcels.
- Thresholds and zone rules (min_area, allowed_zones) are passed in as function parameters, not hardcoded, so the runner controls policy without editing analysis.py.
- Verified correctness in demo.py against the D.4 reasonableness checks: zone counts sum to total parcel count, every development candidate independently satisfies the rule, candidates are a subset of all parcels, and changing min_area changes the result set. 

Part E: Avoid Nested Conditional Chaos 
- Created is_development_candidate to split the responsibility: is_development_candidate is a helper for deciding the rule for single parcel using guard clauses while the development_candidate is for the looping and repetition.
- Verified if the checks on Part D still works. AND IZ OKAY. 
- no rule duplications. the min_area and allowed_zones are already in the is_development_candidate.  

Part F: Spatial Predicate as Part of the Algorithm  
- Updated run_lab4.py using a shapely.geometry.box. This is already wrapped in SpatialObject so it exposes the .intersects() interface as Parcel. 
- No new spatial logic needed since SpatialObject already supports the instantiation.
- Answered the question ("which development candidates also intersect the study area?") by composing existing functions.

Part G: Raster Transfer with Same Control Structures, Different Representation 
- added analysis for the suitability_grid.json, classify_suitability_grid
- added loading of slopes and flood grids.
- added verification if both grids have same rows and columns
- added iteration for processing row then column 
- added condition for 0, 1, and NULL data
- returns the suitability grid and suitable cell count. 
- updated the demo py for checking

Part H: Run the Complete Workflow and Produce Evidence  
- Updated runner to do the following:
    > Load data/parcels_shapely_ready.json. 
    > Construct Parcel objects through the object data boundary. 
    > Stop or report clearly if no valid parcels are loaded. 
    > Set the analysis parameters (threshold, allowed zones, study area). 
    > Call the vector-analysis functions. 
    > Load data/suitability_grid.json and call the raster-analysis functions. 
    > Build a JSON-ready report using IDs/counts/numbers/primitive values. 
    > Write output/lab4_report.json. 
    > Create function for generating output/lab4_vector_preview.png. 
    > Create function for generating output/lab4_raster_preview.png. 

Part I: Testing and Debugging markdown
- Created tests/test_spatial.py and tests/test_analysis.py, using small hand-crafted synthetic parcels/grids instead of the full dataset, so expected outputs can be verified by hand rather than assumed.
- test_spatial.py verifies Parcel.from_dict(...) sets the expected parcel_id, zone, activity, area, and a real Shapely Polygon geometry with a matching bounding box.
- test_analysis.py covers each analysis function individually:
  - total_active_area which excludes an inactive parcel from the sum.
  - parcels_above_threshold includes the exact-threshold case (rule is >=).
  - count_by_zone returns correct per-zone counts for a small mixed sample.
  - development_candidates has **separate** test cases rejecting a parcel for being inactive, for a disallowed zone, and for being under the area minimum and another case confirming a valid parcel is accepted, so a failure points to the exact broken condition instead of one vague "it doesn't work."
  - intersecting_parcels includes one parcel that spatially overlaps a synthetic study area and one that doesn't, confirming both inclusion and exclusion.
  - classify_suitability_grid covers all three output states (1, 0, None/NoData) in one small synthetic grid.
  - count_suitable_cells confirms 0 and None cells are correctly excluded from the count.
MOREOVER~~~~~~~
- Added pytest.ini (pythonpath = src) at the project root so tests/ can import spatial/analysis without path errors, since the project uses a src-layout.
- Verified the I.3 invariants are satisfied by the test set: zone counts sum to total parcels, every returned candidate independently passes active/zone/area checks, and raster output dimensions match input dimensions.
- Ran pytest -v from the project root; all tests pass.


CHALLENGES:
1. Change the Policy Without Rewriting the Algorithm  
    -as shown in demo.py,  when changing the min_area or allowed_zones. the function implementation remains unchanged. 

CODE:  
parcels = [Parcel.from_dict(record) for record in records]  
result_a = development_candidates(parcels, min_area=3000.0, allowed_zones={"Residential", "Commercial"})  
result_b = development_candidates(parcels, min_area=7000.0, allowed_zones={"Residential", "Commercial"})  
print(f"min_area=3000: {len(result_a)} candidates")  
print(f"min_area=7000: {len(result_b)} candidates")  

RESULT:  
min_area=3000: 58 candidates  
min_area=7000: 34 candidates  

2. Compose, Do Not Duplicate 
    - as shown in the run_lab4.py, the development_candidates already narrows the full parcel list down to the ones that pass the active/zone/area rule. The smaller list was simply passed into the intersecting_parcels, which then checks which of those remaining parcels overlap the area. Neither function needed to change, and I didn't have to write the active/zone/area logic a second time anywhere.

CODE:  
    candidates = development_candidates(parcels, MIN_AREA, ALLOWED_ZONES)  
    study_area_candidates = intersecting_parcels(candidates, study_area)  

3. Explain One “Bad vs Good” Refactor  
    - as shown in the analysis.py, before settling the final version of the development_candidates, I have written it in the 'obvious' way like nesting each conditions separately. 
EXAMPLE NESTING:   
START CODE SAMPLE  
for parcel in parcels:  
    if parcel.is_active:  
        if parcel.zone == "Residential":  
            if parcel.area_sqm >= min_area:  
                candidates.append(parcel)  
        elif parcel.zone == "Commercial":  
            if parcel.area_sqm >= min_area:  
                candidates.append(parcel)  
END CODE SAMPLE
    - the problem here is that I'd be writing the same area check once for each zone. To solve this, I created a function and mimic the solution presented on the class before (is_development_candidate). and another solution development_candidate which is only responsible for looping.
GOOD CODE:  
AFTER  
def is_development_candidate(parcel, min_area, allowed_zones): -->mimicked from class last week  
    if not parcel.is_active:  
        return False  
    if parcel.zone not in allowed_zones:  
        return False  
    if parcel.area_sqm < min_area:  
        return False  
    return True  

def development_candidates(parcels, min_area, allowed_zones):  
    candidates = []  
    for parcel in parcels:  
        if is_development_candidate(parcel, min_area, allowed_zones):  
            candidates.append(parcel)  
    return candidates   

4.  Transfer the Algorithmic Pattern 
    - comparing the vector loop and raster loop.

CODE COMPARISON:  
# Vector  
for parcel in parcels:  
    if is_development_candidate(parcel, min_area, allowed_zones):  
        candidates.append(parcel)  

# Raster  
for r in range(rows):    
    for c in range(cols):  
        if slope_grid[r][c] is None or flood_grid[r][c] is None:  
            result_row.append(None)  
        elif slope_grid[r][c] <= max_slope and flood_grid[r][c] <= max_flood:  
            result_row.append(1)  
        else:  
            result_row.append(0)  
END COMPARISON  
    - The code followed similar structure for loading data first -> analyze it -> report (in that order). Also in both cases, the thresholds are set as parameters which are not hardcoded in the function. 
    - The code differs from the data shape: The parcel is flat so a single loop would suffice while the raster is 2-dimensional, meaning it needs a loop for the rows and another for the columns. 
    - Another difference is that the Parcel is an object that can answer questions itself like parcel.is_active or parcel.intersects(). While the raster, I have to write out the suitability logic since the raster only contains values with no behavior on its own. 


# Reflections  
1. ALGORITHM. For the development_candidates question, writing the pseudocode helped me decide what the variables do I use, the conditions need to set, and the return type before actually implementing it in Python. When I'm implementing it, there wasn't much to change since the Python change is simply a translation not the designing itself.

2. CONTROL FLOW. The sequence appears as load -> construct -> validate -> analyze -> loop -> report. Selection appears inside the is_development_candidate's guard clauses and inside classify_suitability_grid's NoData/threshold checks.  And Lastly, repetition appears as the single for-loop over parcels in each analysis.py function, and as the nested for-loops over rows/columns in classify_suitability_grid.

3. RESPONSIBILITY. Parcel.intersects(...) belongs to the object layer because the overlap is a fact about the geometry itself and the rule "active AND zone in {Residential, Commercial} AND area >= 5000" belongs to analysis.py because it is a project-specific decision, not an inherent property of the Parcel. 

4. CONDITIONAL STRUCTURE. Splitting development_candidates into a guard-clause helper(is_development_candidate) and a separate coordinating loop prevents nested chaos. Each condition in the helper is an independent early return not nested inside the previous one, so the function reads as a flat checklist. Adding a new criterion means adding one more guard-clause line and not another indentation level.

5. AREA MEANING. The parcel coordinates are longitude/latitude in degrees while Shapely's
geometry.area computes planar area from whatever numbers it's given, with no awareness that these are angular coordinates on a curved earth. Moreover, area_sqm is a precomputed, trustworthy value already in the dataset, so it's the only value used for area throughout the project. 

6. VECTOR VS RASTER. As mentioned in the challenges before, repetition over parcels is a single loop, because a list is already flat. Repetition over the rastergrid needs two nested loops (row, then column), because a 2D grid can't be reached with one loop. Both loops visit every unit exactly once, both ask one selection question per unit, and both keep policy values (thresholds, zones) as parameters rather than hardcoded constants.


7. SCALE. The parameter arguments design and the guard-clause structure would remain useful since they don't depende on parcel or cell size. At a million parcel or at a 10000 by 10000 raster, the processing would be extremely slow and would need the help of indexing or an array library (like NumPy) to make processing efficient.


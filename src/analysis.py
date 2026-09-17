#following the PSEUDOCODE


def total_active_area(parcels):
    total = 0.0
    for parcel in parcels:
        if parcel.is_active:
            total += parcel.area_sqm
    return total

def parcels_above_threshold(parcels, threshold):
    result = []
    for parcel in parcels:
        if parcel.area_sqm >= threshold:
            result.append(parcel)
    return result

def count_by_zone(parcels):
    counts = {}
    for parcel in parcels:
        if parcel.zone not in counts:
            counts[parcel.zone] = 0
        counts[parcel.zone] += 1
    return counts

def is_development_candidate(parcel, min_area, allowed_zones):
    #added to avoid nesting
    if not parcel.is_active:
        return False
    if parcel.zone not in allowed_zones:
        return False
    if parcel.area_sqm < min_area:
        return False
    return True

def development_candidates(parcels, min_area, allowed_zones):
    #updated by calling another function 
    candidates = []
    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)
    return candidates

def intersecting_parcels(parcels, study_area):
    result = []
    for parcel in parcels:
        if parcel.intersects(study_area):
            result.append(parcel)
    return result

def classify_suitability_grid(slope_grid, flood_grid, max_slope, max_flood):
    '''
    Builds a new grid, same dimensions, where each cell is 1 (suitable), 
    0 (not suitable), or None (NoData in either input)
    '''
    rows = len(slope_grid)
    cols = len(slope_grid[0])

    if len(flood_grid) != rows or any(len(row) != cols for row in flood_grid):#check if they have matching dimensions
        raise ValueError("slope_grid and flood_grid must have matching dimensions")
    
    result = []
    for r in range(rows):
        result_row = []
        for c in range(cols):
            slope = slope_grid[r][c]
            flood = flood_grid[r][c]
            if slope is None or flood is None:
                result_row.append(None)
            elif slope <= max_slope and flood <= max_flood:
                result_row.append(1)
            else:
                result_row.append(0)
        result.append(result_row)
    return result

def count_suitable_cells(suitability_grid):
    '''
    counts how many 1s are in that output grid, using an explicit loop
    '''
    count = 0
    for row in suitability_grid:
        for cell in row:
            if cell == 1:
                count += 1
    return count
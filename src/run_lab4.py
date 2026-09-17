import json
import matplotlib.pyplot as plt
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


def save_vector_preview(parcels, candidates, study_area):
    '''
    For vector plotting and saving
    '''
    candidate_ids = {p.parcel_id for p in candidates}

    fig, ax = plt.subplots(figsize=(8, 8))
    for parcel in parcels:
        x, y = parcel.geometry.exterior.xy
        color = "orange" if parcel.parcel_id in candidate_ids else "gray"
        ax.fill(x, y, facecolor=color, edgecolor="black", alpha=0.5, linewidth=0.5)

    sx, sy = study_area.geometry.exterior.xy
    ax.plot(sx, sy, color="blue", linewidth=2, label="Study area")

    ax.set_title("Lab 4 Vector Preview — Development Candidates Highlighted")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    fig.savefig("output/lab4_vector_preview.png", dpi=150)
    plt.close(fig)


def save_raster_preview(suitability_grid):
    '''
    For raster plotting and saving
    '''
    display_grid = [
        [float("nan") if cell is None else cell for cell in row]
        for row in suitability_grid
    ]

    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(display_grid, cmap="RdYlGn", vmin=0, vmax=1)
    ax.set_title("Suitability(Green=Suitable, Red=Not, blank=NoData)")
    fig.savefig("output/lab4_raster_preview.png", dpi=150)
    plt.close(fig)

def main():
    # 1. load external data
    with open("data/parcels_shapely_ready.json", encoding="utf-8") as f:
        records = json.load(f)

    # 2. construct Parcel objects
    parcels = [Parcel.from_dict(record) for record in records]

    # 3. validate that required inputs exist
    if not parcels:
        print("No valid parcels loaded — aborting.")
        return

    # 4. define analysis parameters
    THRESHOLD = 5000.0
    MIN_AREA = 5000.0
    ALLOWED_ZONES = {"Residential", "Commercial"}
    study_area = SpatialObject(box(121.050, 14.648, 121.060, 14.658))

    # 5. call vector-analysis functions
    active_area = total_active_area(parcels)
    above_threshold = parcels_above_threshold(parcels, THRESHOLD)
    zone_counts = count_by_zone(parcels)
    candidates = development_candidates(parcels, MIN_AREA, ALLOWED_ZONES)
    study_area_candidates = intersecting_parcels(candidates, study_area)

    # 6. call raster-analysis functions
    with open("data/suitability_grid.json", encoding="utf-8") as f:
        grid_data = json.load(f)

    criteria = grid_data["criteria"]
    suitability_grid = classify_suitability_grid(
        grid_data["slope_deg"],
        grid_data["flood_m"],
        max_slope=criteria["max_slope_deg"],
        max_flood=criteria["max_flood_m"],
    )
    suitable_count = count_suitable_cells(suitability_grid)

    # 7. assemble JSON-ready report
    report = {
        "vector": {
            "parcel_count": len(parcels),
            "total_active_area_sqm": active_area,
            "zone_counts": zone_counts,
            "above_threshold_ids": [p.parcel_id for p in above_threshold],
            "candidate_ids": [p.parcel_id for p in candidates],
            "study_area_candidate_ids": [p.parcel_id for p in study_area_candidates],
        },
        "raster": {
            "rows": len(suitability_grid),
            "cols": len(suitability_grid[0]),
            "suitable_cell_count": suitable_count,
            "suitability_grid": suitability_grid,
        },
    }

    # 8. write report and figures
    with open("output/lab4_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    save_vector_preview(parcels, candidates, study_area)
    save_raster_preview(suitability_grid)

    print(f"Loaded {len(parcels)} parcels, {len(candidates)} candidates, "
          f"{len(study_area_candidates)} inside study area.")
    print(f"Suitable raster cells: {suitable_count}")


if __name__ == "__main__":
    main()
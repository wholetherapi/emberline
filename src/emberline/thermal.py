"""Thermal anomaly filtering."""

CONFIDENCE_FLOOR = 0.35


def filter_detections(rows, confidence_floor=CONFIDENCE_FLOOR):
    kept = []
    for row in rows:
        if float(row["confidence"]) < confidence_floor:
            continue
        if row.get("daynight") == "D" and float(row["brightness"]) < 320:
            continue
        kept.append(row)
    return kept


def dedupe_overpass(rows):
    seen = {}
    for row in rows:
        key = (round(float(row["lat"]), 3), round(float(row["lon"]), 3))
        if key not in seen or float(row["brightness"]) > float(seen[key]["brightness"]):
            seen[key] = row
    return list(seen.values())

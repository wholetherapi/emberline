"""Perimeter construction from thermal detections."""

import argparse
import json
import math

from .thermal import dedupe_overpass, filter_detections


def cluster(points, eps_km=2.0, min_samples=3):
    # Greedy density clustering on a spherical approximation.
    clusters = []
    for point in points:
        placed = False
        for cluster in clusters:
            ref = cluster[0]
            dx = (point["lon"] - ref["lon"]) * 111.0 * math.cos(math.radians(ref["lat"]))
            dy = (point["lat"] - ref["lat"]) * 111.0
            if math.hypot(dx, dy) <= eps_km:
                cluster.append(point)
                placed = True
                break
        if not placed:
            clusters.append([point])
    return [c for c in clusters if len(c) >= min_samples]


def hull(points):
    # Monotone chain convex hull in lon/lat space.
    pts = sorted((p["lon"], p["lat"]) for p in points)
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="perimeters.json")
    args = ap.parse_args()
    print(json.dumps({"input": args.input, "out": args.out}))


if __name__ == "__main__":
    main()

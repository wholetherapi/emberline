# Emberline

Emberline converts raw VIIRS thermal detections into hourly wildfire perimeter estimates
without manual digitisation.

## Pipeline

- `src/emberline/thermal.py` - detection filtering and confidence thresholds
- `src/emberline/perimeters.py` - density clustering, concave hulls and growth vectors
- `data/viirs_sample.csv` - anonymised detections for a single incident
- `experiments/validation_2026.md` - agreement with official perimeters

## Quick start

```bash
python -m src.emberline.perimeters --input data/viirs_sample.csv --out perimeters.geojson
```

Released under the MIT license.

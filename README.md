# Running Workout Parser

## Foreward
I let chat write a README for this script. Results are good I think.

## Overview
This script parses running workout data from Apple Health XML export files (`export.xml`) and converts them into a JSON format. It removes duplicate workouts based on the `startDate` and supports multiple input files.

## Requirements
- Python 3.x

## Usage
Run the script using the following command:

```bash
python script.py --paths /path/to/export1.xml /path/to/export2.xml --out /path/to/output.json
```

### Arguments:
- `--paths` (required): One or more paths to `export.xml` files.
- `--out` (required): Path to the output JSON file.

## Example
```bash
python script.py --paths data/export1.xml data/export2.xml --out output/workouts.json
```
This will parse `export1.xml` and `export2.xml`, remove duplicate workouts, and save the processed data to `output/workouts.json`.

## Output Format
The JSON output contains an array of workout objects with attributes and statistics:

```json
[
    {
        "workoutActivityType": "HKWorkoutActivityTypeRunning",
        "startDate": "2024-01-01T10:00:00Z",
        "endDate": "2024-01-01T11:00:00Z",
        "duration": "3600",
        "stats": [
            {
                "type": "HKQuantityTypeIdentifierDistanceWalkingRunning",
                "value": "5.0",
                "unit": "km"
            }
        ]
    }
]
```



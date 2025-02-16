import argparse
import json
import os
import xml.etree.ElementTree as ET

def remove_duplicate_workouts(workouts):
    """Removes duplicate workouts based on startDate."""
    unique_workouts = {}
    
    for workout in workouts:
        start_date = workout['startDate']
        if start_date in unique_workouts:
            print(f"Duplicate workout found, startDate: {start_date}, skipping.")
        else:
            unique_workouts[start_date] = workout
    
    return list(unique_workouts.values())

def parse_workout_data(file_path):
    """Parses a single Apple Health XML file for running workouts."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        workouts = []

        for workout in root.findall('Workout'):
            if workout.attrib.get('workoutActivityType') != "HKWorkoutActivityTypeRunning":
                continue
            
            workout_stats = {
                **workout.attrib,
                "stats": [stat.attrib for stat in workout.findall("WorkoutStatistics")]
            }
            workouts.append(workout_stats)
        
        return workouts
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except ET.ParseError as e:
        print(f"Error: Invalid XML format in {file_path}: {e}")
    
    return []

def parse_running_data(file_paths, out_path):
    """Parses running workout data from multiple XML files and saves to JSON."""
    all_workouts = []
    
    for file_path in file_paths:
        all_workouts.extend(parse_workout_data(file_path))
    
    if len(file_paths) > 1:
        print(f"{len(file_paths)} export files processed. Removing duplicates...")
        all_workouts = remove_duplicate_workouts(all_workouts)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as file:
        json.dump(all_workouts, file, indent=4)
    
    print(f"Processed {len(all_workouts)} unique workouts. Output saved to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse running workouts from Apple Health data export.')
    parser.add_argument('--paths', nargs='+', required=True, help="Paths to export.xml, multiple arguments accepted.")
    parser.add_argument('--out', required=True, help="Path to output file")
    args = parser.parse_args()
    
    parse_running_data(args.paths, args.out)


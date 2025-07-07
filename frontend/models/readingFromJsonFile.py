import json
import re
import glob
import os # Import os for path manipulation, though pathlib is also an option

SAMPLE_ITEMS = [] # Initialize as an empty list to collect data from all files
sections = set()

# Define the directory where your JSON files are located.
# '.' refers to the current directory where the script is being run.
# You can change this to a specific path like 'C:/path/to/your/json_files/'
json_files_directory = './test_data'

# Use glob to find all .json files in the specified directory
# The full path of each file will be returned
json_file_paths = glob.glob(os.path.join(json_files_directory, '*.json'))

print(f"Found {len(json_file_paths)} JSON files to process.")

for file_path in json_file_paths:
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonFile:
            # Load each JSON file and extend SAMPLE_ITEMS
            data = json.load(jsonFile)
            # Ensure 'data' is a list if SAMPLE_ITEMS expects a list of items.
            # If each JSON file contains a single object, you might need to append.
            # Assuming each file might contain a list of items or a single item:
            if isinstance(data, list):
                SAMPLE_ITEMS.extend(data)
            else:
                SAMPLE_ITEMS.append(data)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        continue # Skip to the next file if there's an error
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        continue
    except Exception as e:
        print(f"An unexpected error occurred with {file_path}: {e}")
        continue

# Now, process all collected items
for j in SAMPLE_ITEMS:
    # Add a check to ensure 'resourceType' key exists to prevent KeyError
    if 'resourceType' in j:
        sectionNameSeperated = re.sub(r"(\w)([A-Z])", r"\1 \2", j['resourceType'])
        j['resourceType'] = sectionNameSeperated
        sections.add(j['resourceType'])
    else:
        print(f"Warning: Item missing 'resourceType' key: {j}")


LIST_OF_SECTIONS = sorted(list(sections)) # Convert set to list for sorting

print(f"\nProcessed a total of {len(SAMPLE_ITEMS)} items.")
print("List of unique sections found:")
for section in LIST_OF_SECTIONS:
    print(f"- {section}")

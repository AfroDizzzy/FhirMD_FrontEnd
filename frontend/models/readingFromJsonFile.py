import json
import re
import glob
import os

# Global lists/sets
SAMPLE_ITEMS = []
sections = set()

# Define the directory where your JSON/MD files are located.
json_files_directory = './test_data'

print(f"Checking for data files in: {os.path.abspath(json_files_directory)}") #

# Temporary storage to link JSON and metadata by filename
temp_items_by_filename = {}

# --- First Pass: Read all .json files ---
json_file_paths = glob.glob(os.path.join(json_files_directory, '*.json')) #
print(f"Found {len(json_file_paths)} JSON files to process.") #

for file_path in json_file_paths: #
    base_filename = os.path.basename(file_path) #
    try: #
        with open(file_path, 'r', encoding='utf-8') as jsonFile: #
            data = json.load(jsonFile) #
            if isinstance(data, dict): #
                temp_items_by_filename[base_filename] = data #
            else: #
                print(f"Warning: Skipping non-dict JSON content in {file_path}") #

    except json.JSONDecodeError as e: #
        print(f"Error decoding JSON from {file_path}: {e}") #
        continue #
    except FileNotFoundError: #
        print(f"File not found: {file_path}") #
        continue #
    except Exception as e: #
        print(f"An unexpected error occurred with {file_path}: {e}") #
        continue #

# --- Second Pass: Read all .md files and associate metadata ---
md_file_paths = glob.glob(os.path.join(json_files_directory, '*.md')) #
print(f"Found {len(md_file_paths)} MD (metadata) files to process.") #

for md_file_path in md_file_paths: #
    try: #
        with open(md_file_path, 'r', encoding='utf-8') as mdFile: #
            metadata = json.load(mdFile) #

            associated_json_filename = metadata.get('filename') #

            if associated_json_filename and associated_json_filename in temp_items_by_filename: #
                # Change '_metadata' to 'file_metadata'
                temp_items_by_filename[associated_json_filename]['file_metadata'] = metadata #
            else: #
                print(f"Warning: Metadata file {md_file_path} has no 'filename' field or "
                      f"associated JSON '{associated_json_filename}' not found.") #

    except json.JSONDecodeError as e: #
        print(f"Error decoding JSON from MD file {md_file_path}: {e}") #
        continue #
    except FileNotFoundError: #
        print(f"MD file not found: {md_file_path}") #
        continue #
    except Exception as e: #
        print(f"An unexpected error occurred with MD file {md_file_path}: {e}") #
        continue #

# --- Final step: Populate SAMPLE_ITEMS and sections from the combined data ---
for filename, item_data in temp_items_by_filename.items(): #
    SAMPLE_ITEMS.append(item_data) #
    if 'resourceType' in item_data: #
        sectionNameSeperated = re.sub(r"(\w)([A-Z])", r"\1 \2", item_data['resourceType']) #
        item_data['resourceType'] = sectionNameSeperated #
        sections.add(sectionNameSeperated) #
    else: #
        print(f"Warning: Item from {filename} missing 'resourceType' key: {item_data}") #


LIST_OF_SECTIONS = sorted(list(sections)) #

print(f"\nProcessed a total of {len(SAMPLE_ITEMS)} items.") #
print("List of unique sections found:") #
for section in LIST_OF_SECTIONS: #
    print(f"- {section}") #
import json
import re
import glob
import os

# Global variables that will be populated
SAMPLE_ITEMS = []
sections = set()
LIST_OF_SECTIONS = [] # Initialize as empty list

# Define the directory where your JSON/MD files are located.
# IMPORTANT: This path needs to be writable by the 'appuser' in Docker.
json_files_directory = './test_data'

# Function to load/reload all data
def load_all_data():
    global SAMPLE_ITEMS, sections, LIST_OF_SECTIONS
    SAMPLE_ITEMS = [] # Clear existing data
    sections = set() # Clear existing sections
    LIST_OF_SECTIONS = []

    print(f"Loading data from: {os.path.abspath(json_files_directory)}")

    temp_items_by_filename = {}

    # --- First Pass: Read all .json files ---
    json_file_paths = glob.glob(os.path.join(json_files_directory, '*.json'))
    print(f"Found {len(json_file_paths)} JSON files to process.")

    for file_path in json_file_paths:
        base_filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
                # Assuming each JSON file contains a single item/object at its root
                if isinstance(data, dict):
                    temp_items_by_filename[base_filename] = data
                else:
                    print(f"Warning: Skipping non-dict JSON content in {file_path}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            continue
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred with {file_path}: {e}")
            continue

    # --- Second Pass: Read all .md files and associate metadata ---
    md_file_paths = glob.glob(os.path.join(json_files_directory, '*.md'))
    print(f"Found {len(md_file_paths)} MD (metadata) files to process.")

    for md_file_path in md_file_paths:
        try:
            with open(md_file_path, 'r', encoding='utf-8') as mdFile:
                metadata = json.load(mdFile)
                associated_json_filename = metadata.get('filename')

                if associated_json_filename and associated_json_filename in temp_items_by_filename:
                    temp_items_by_filename[associated_json_filename]['file_metadata'] = metadata
                else:
                    print(f"Warning: Metadata file {md_file_path} has no 'filename' field or "
                          f"associated JSON '{associated_json_filename}' not found.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from MD file {md_file_path}: {e}")
            continue
        except FileNotFoundError:
            print(f"MD file not found: {md_file_path}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred with MD file {md_file_path}: {e}")
            continue

    # --- Final step: Populate SAMPLE_ITEMS and sections from the combined data ---
    for filename, item_data in temp_items_by_filename.items():
        SAMPLE_ITEMS.append(item_data)
        if 'resourceType' in item_data:
            sectionNameSeperated = re.sub(r"(\w)([A-Z])", r"\1 \2", item_data['resourceType'])
            item_data['resourceType'] = sectionNameSeperated
            sections.add(sectionNameSeperated)
        else:
            print(f"Warning: Item from {filename} missing 'resourceType' key: {item_data}")

    LIST_OF_SECTIONS = sorted(list(sections))

    print(f"\nProcessed a total of {len(SAMPLE_ITEMS)} items.")
    print("List of unique sections found:")
    for section in LIST_OF_SECTIONS:
        print(f"- {section}")

# Call load_all_data once when the module is imported
load_all_data()

# Helper function for the admin page to get all JSON filenames and their metadata status
def get_all_json_filenames_with_metadata_status():
    json_files = []
    all_json_filepaths = glob.glob(os.path.join(json_files_directory, '*.json'))
    all_md_filepaths = glob.glob(os.path.join(json_files_directory, '*.md'))
    md_filenames = {os.path.basename(f) for f in all_md_filepaths}

    for json_filepath in all_json_filepaths:
        base_filename = os.path.basename(json_filepath)
        md_filename = base_filename.replace('.json', '.md') # Assuming .md is same base name
        has_metadata = os.path.exists(os.path.join(json_files_directory, md_filename)) # Check existence on disk
        json_files.append({
            'filename': base_filename,
            'has_metadata': has_metadata,
            'md_filename': md_filename # Store the expected MD filename
        })
    return sorted(json_files, key=lambda x: x['filename'])
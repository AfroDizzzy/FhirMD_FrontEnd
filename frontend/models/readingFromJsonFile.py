import json
import re
import glob
import os

# Global variables that will be populated
SAMPLE_ITEMS = []
sections = set()
LIST_OF_SECTIONS = []

# Define the directory where your JSON/MD files are located.
json_files_directory = './test_data'

# Helper to parse IG_Notation string
def parse_ig_notation_string(ig_notation_str):
    parsed_igs = []
    
    if not isinstance(ig_notation_str, str):
        return parsed_igs
    """
    Parses a comma-separated IG notation string (e.g., "name:version,name2:version2")
    into a list of dictionaries [{'name': '...', 'version': '...'}].
    """
    entries = [entry.strip() for entry in ig_notation_str.split(',') if entry.strip()]
    for entry in entries:
        parts = entry.split(':', 1) # Split only on the first colon
        ig_name = parts[0].strip()
        ig_version = parts[1].strip() if len(parts) > 1 else ""
        parsed_igs.append({'name': ig_name, 'version': ig_version})
    return parsed_igs

# Function to load/reload all data
def load_all_data():
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
                if isinstance(data, dict):
                    temp_items_by_filename[base_filename] = data
                else:
                    print(f"Warning: Skipping non-dict JSON content in {file_path}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            continue
        except FileNotFoundError: # This should not happen with glob, but good for robustness
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
                    # Add raw metadata
                    temp_items_by_filename[associated_json_filename]['file_metadata'] = metadata

                    # NEW: Process IG_Notation and store as Parsed_IG_Notations
                    ig_notation_str = metadata.get('IG_Notation')
                    if ig_notation_str:
                        temp_items_by_filename[associated_json_filename]['file_metadata']['Parsed_IG_Notations'] = \
                            parse_ig_notation_string(ig_notation_str)
                    else:
                        # Fallback for old structure: combine IG and IG_Version if IG_Notation not present
                        old_ig = metadata.get('IG')
                        old_ig_version = metadata.get('IG_Version')
                        if old_ig:
                            fallback_notation = f"{old_ig}:{old_ig_version or 'unknown'}"
                            temp_items_by_filename[associated_json_filename]['file_metadata']['Parsed_IG_Notations'] = \
                                parse_ig_notation_string(fallback_notation)


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
    # Use os.path.exists for specific .md file, more accurate than globbing all .md files first
    for json_filepath in all_json_filepaths:
        base_filename = os.path.basename(json_filepath)
        md_filename = base_filename.replace('.json', '.md')
        has_metadata = os.path.exists(os.path.join(json_files_directory, md_filename))
        json_files.append({
            'filename': base_filename,
            'has_metadata': has_metadata,
            'md_filename': md_filename
        })
    return sorted(json_files, key=lambda x: x['filename'])
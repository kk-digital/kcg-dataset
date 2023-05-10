import os
import zipfile
import hashlib
import time
import argparse
import json
from tqdm import tqdm

def process_zip_files(input_directory, output_directory):
    zip_files = [os.path.join(root, file) for root, _, files in os.walk(input_directory) for file in files if file.endswith('.zip')]
    total_zip_files = len(zip_files)
    print(f"Processing {total_zip_files} zip files...")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i, zip_file_path in enumerate(tqdm(zip_files, desc="Processing zip files")):
        start_time = time.time()
        file_data = []
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    with zip_ref.open(file_info) as file:
                        file_data.append({
                            'file_path': os.path.join(os.path.dirname(zip_file_path), file_info.filename),
                            'file_name': os.path.basename(file_info.filename),
                            'sha256': hashlib.sha256(file.read()).hexdigest()
                        })
            process_time = time.time() - start_time
            zip_file_size = os.path.getsize(zip_file_path) / (1024 * 1024)  # size in MB
            speed = zip_file_size / process_time  # speed in MB/s

            print(f"Processed zip file '{zip_file_path}' ({zip_file_size:.2f} MB) in {process_time:.2f} seconds ({speed:.2f} MB/s).")

            # save output to a JSON file
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(zip_file_path))[0]}.json")
            with open(output_file_path, 'w') as f:
                json.dump(file_data, f, indent=4)

        except Exception as e:
            print(f"Error processing zip file '{zip_file_path}': {e}")

        # Print the progress for the current zip file being processed
        if i == 0:
            progress = f"1/{total_zip_files}"
        else:
            progress = f"{i+1}/{total_zip_files}"
        print(f"\nProcessed {progress} zip files.\n")

    print("Processing finished.")

parser = argparse.ArgumentParser(description='Process zip files in a directory.')
parser.add_argument('input_directory', type=str, help='Path to directory containing zip files')
parser.add_argument('output_directory', type=str, help='Path to directory where output JSON files will be saved')

args = parser.parse_args()
process_zip_files(args.input_directory, args.output_directory)

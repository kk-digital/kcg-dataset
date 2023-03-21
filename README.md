# kcg-dataset

There are two scripts in this repository:

1 - `image_sorter.py` sorts the extracted AVA dataset images and arrange them in the directories. To run 
`cd AVA`
`python3 ~/repo/kcg-datasets/ava-tools/image_sorter.py`

2 - `ava_json_generator.py` converts the AVA from the original txt format to JSON format. It will also read the images from the sorted image directories and add their correspoding JSON files in that directories.
`cd AVA`
`python3 ~/repo/kcg-datasets/ava-tools/ava-json-generator.py`

3 - `clip_generator.py` adds the clip vectors for each image in the corresponding JSON file. This script uses AVA.json file generated from `ava_json_generator.py`.
`cd AVA`
`python3 ~/repo/kcg-datasets/ava-tools/clip-generator.py`

4 - `zip_generator.py` generates zip files from the given directories.

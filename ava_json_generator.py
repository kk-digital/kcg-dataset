import os
import json
import hashlib
import pandas as pd

# set the directory paths
IMAGES_DIR = 'images-sorted'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) # use the dataset is in the same directory as the script
SCRIPT_DIR = os.getcwd() # use this if dataset is in the current working directory

# set INDENT to None to create a single line JSON file
INDENT = 1

# Read in the data
df = pd.read_csv('AVA.txt', sep=' ',header=None)

# list of column names
COL_NAMES = ['Index', 'ImageId', '1', '2', '3', '4', '5', '6', '7','8','9','10','SemanticTag_1','SemanticTag_2','ChallengeId']

# set the column names
df.columns = COL_NAMES

# add an empty column for the image hash
df['FileHash'] = ''
# add an empty column for the image file name
df['FileName'] = ''
# add ScoreCount column
df['ScoreCount'] = df.loc[:, '1':'10'].sum(axis=1)
# add a dictionary column for the for image ratings
df['ScoreDictionary'] = df.loc[:, '1':'10'].to_dict(orient='records')
# drop the columns for the image ratings
df.drop(df.loc[:, '1':'10'], axis=1, inplace=True)
# drop the columns for the semantic tags and challenge id
df.drop(df.loc[:, 'SemanticTag_1':'ChallengeId'], axis=1, inplace=True)

# set the index to the ImageId
df.set_index('ImageId', inplace=True, drop=False)

# sort the dataframe by the index
df.sort_index(inplace=True)

naming_convention = 'dataset-ava'

# create an empty dataframe
df_new = pd.DataFrame(columns=df.columns)

# iterate through the directories
directories = os.listdir(IMAGES_DIR)
# sort the directories
directories = sorted(directories)
print(f'Total number of directories: {len(directories)}')

for directory in directories:
    print(f'Processing directory: {directory}')
    # iterate through the files in the directory
    files = os.listdir(os.path.join(IMAGES_DIR, directory))
    total_files = len(files)

    # create an empty dataframe
    df_new = pd.DataFrame(columns=df.columns)

    for index, file in enumerate(files):
        # print the progress
        print(f"Processing file {index+1}/{total_files}", end='\r')
        # check if the file is an image
        if not file.endswith('.jpg') and not file.endswith('.png'):
            continue

        # read in the file
        path = os.path.join(IMAGES_DIR, directory, file)
        with open(path, 'rb') as f:
            img = f.read()

        # calculate the hash
        hash = hashlib.sha256(img).hexdigest()

        # get the image id
        image_id = int(file.split('.')[0])

        # insert the hash and file name into the dataframe
        df.loc[image_id, 'FileHash'] = hash
        df.loc[image_id, 'FileName'] = file

        # append the row to the new dataframe
        df_new = pd.concat([df_new, df.loc[[image_id]]])

    # set the index to the ImageId
    df_new.set_index('ImageId', inplace=True, drop=False)

    # save the dataframe to a json file
    path = os.path.join(SCRIPT_DIR, IMAGES_DIR, directory, directory)
    df_new.to_json(f'{path}.json', orient='records', indent=INDENT)

# write the AVA dataframe to a json file with the image hashes
df_found = df[df['FileHash'] != '']
df_found.to_json('AVA.json', orient='records', indent=INDENT)
# write error.txt
df_not_found = df[df['FileHash'] == '']
with open('error.txt', 'w') as f:
    f.write(df_not_found.loc[:, ['Index', 'ImageId']].to_string(header=True, index=False))

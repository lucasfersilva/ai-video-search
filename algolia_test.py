import algoliasearch.exceptions
import requests
from algoliasearch.search_client import SearchClient
import os
import json


def get_filenames_in_folder(folder_path):
    filenames_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file_path is a file (not a subdirectory)
        if os.path.isfile(file_path):
            filenames_list.append(filename)

    return filenames_list


filenames = get_filenames_in_folder('parsed_jsons')
failed_list =[]
for i in filenames:
    if i == '.DS_Store':
        continue
    print(i)
    client = SearchClient.create(
        'APP-ID',
        'CREDENTIAL'
    )

    video_intelligence = json.load(open(f'parsed_jsons/{i}'))

    index = client.init_index("push_data")

    try:
        index.save_objects(video_intelligence,{'autoGenerateObjectIDIfNotExist':True}).wait()

    except algoliasearch.exceptions.RequestException:
        failed_list.append(i)

print(failed_list)

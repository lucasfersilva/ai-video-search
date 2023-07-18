from google.cloud import storage
from google.cloud.storage import Blob
import os

storage_client = storage.Client('even-research-392016')
blobs = storage_client.list_blobs('videos_intelligence')


def check_json():
    json_folder = './parsed_jsons/'
    for blob in blobs:
        file_extension = os.path.splitext(blob.name)[1]
        size_in_kb = (blob.size/1024 * 1024)
        formatted_size = "{:.4f}".format(size_in_kb)
        if file_extension != '.json':
            continue
        if os.path.isfile(json_folder + blob.name):
            print(f"The file {blob.name} already exists in the path")
        else:
            print(f"The file {blob.name} does not exists it will download, it has {formatted_size} mbs")
            filename = str(blob.name)
            with open(json_folder + filename,'wb') as file_obj:
                destination = json_folder + str(filename)
                blob.download_to_filename(destination)



check_json()
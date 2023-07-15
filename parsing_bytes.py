import os
import json
import uuid


def get_filenames_in_folder(folder_path):
    filenames_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file_path is a file (not a subdirectory)
        if os.path.isfile(file_path):
            filenames_list.append(filename)

    return filenames_list


def split_json_into_files(json_data, output_folder, max_file_size_bytes):
    # Serialize the data to JSON
    algolia_data = []
    for index, result in enumerate(json_data['annotation_results']):
        video_id = result['input_uri']
        title = result['input_uri']  # You can modify this to match your desired title field

        # Combine relevant information from different features
        description = ''
        label = ''
        annotations = ''
        video_transcription = ''

        if 'segment_label_annotations' in result:
            for label_annotation in result['segment_label_annotations']:
                label += label_annotation['entity']['description'] + ' '

        if 'text_annotations' in result:
            for text_annotation in result['text_annotations']:
                annotations += text_annotation['text'] + ' '

        if 'speech_transcriptions' in result:
            for transcription in result['speech_transcriptions']:
                alternatives = transcription.get('alternatives', [])
                if alternatives:
                    for alternative in alternatives:
                        video_transcription += alternative.get('transcript', '') + ' '

        unique = uuid.uuid4().int
        # Create an Algolia-formatted object
        algolia_object = {
            # 'objectID': unique,  # Removed 'objectID' field as it's not necessary
            'video_id': video_id,
            'title': title,
            'labels': label,
            'annotations': annotations,
            'transcription': video_transcription
        }

        algolia_data.append(algolia_object)

    # Split the Algolia objects into multiple files based on max_file_size_bytes
    current_file_size = 0
    current_file_index = 1
    current_file_objects = []

    for algolia_object in algolia_data:
        algolia_object_size = len(json.dumps(algolia_object))
        if current_file_size + algolia_object_size > max_file_size_bytes:
            create_json_file(
                os.path.join(output_folder, f"parsed_jsons_part_{current_file_index}.json"),
                current_file_objects
            )
            current_file_index += 1
            current_file_objects = []
            current_file_size = 0

        current_file_objects.append(algolia_object)
        current_file_size += algolia_object_size

    # Save any remaining objects to a new file
    if current_file_objects:
        create_json_file(
            os.path.join(output_folder, f"parsed_jsons_part_{current_file_index}.json"),
            current_file_objects
        )


def create_json_file(file_path, algolia_objects):
    with open(file_path, 'w') as json_file:
        json.dump(algolia_objects, json_file)


if __name__ == "__main__":
    input_folder = 'commom json'
    output_folder = 'parsed_jsons'
    max_file_size_bytes = 10000

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    filenames = get_filenames_in_folder(input_folder)

    for i in filenames:
        if i == '.DS_Store':
            continue

        print(i)

        json_path = os.path.join(input_folder, i)

        with open(json_path) as json_file:
            data = json.load(json_file)

        # Split and save JSON into multiple files
        split_json_into_files(data, output_folder, max_file_size_bytes)

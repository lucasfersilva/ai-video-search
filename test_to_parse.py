import os

def get_filenames_in_folder(folder_path):
    filenames_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file_path is a file (not a subdirectory)
        if os.path.isfile(file_path):
            filenames_list.append(filename)

    return filenames_list


filenames = get_filenames_in_folder('commom json')

for i in filenames:
    if i == '.DS_Store':
        continue

    print(i)

    import json
    import random
    import uuid

    json_path = f'commom json/{i}'

    with open(json_path) as json_file:
        data = json.load(json_file)

    algolia_data = []
    for index, result in enumerate(data['annotation_results']):
        video_id = result['input_uri']
        title = result['input_uri']  # You can modify this to match your desired title field

        # Combine relevant information from different features
        description = ''
        label = ''
        annotations = ''
        video_transcription = ''
        start_time_seconds = 0
        transcription_with_seconds = []
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
                        words = alternative.get('words', [])
                        for word in words:
                            # Get seconds from the 'start_time' field inside 'words'
                            start_time_seconds = word['start_time'].get('seconds', None)
                            if start_time_seconds is not None:
                                # Do something with the seconds value here
                                #print("Word Start Time Seconds:", start_time_seconds)
                                transcription_with_seconds.append({
                                    'transcription': word['word'],
                                    'start_time_seconds': start_time_seconds
                                })
                                print(transcription_with_seconds)

        unique = uuid.uuid4().int
        # Create an Algolia-formatted object
        algolia_object = {
            #'objectID': unique,
            'video_id': video_id,
            'title': title,
            'labels': label,
            'annotations': annotations,
            'transcription': video_transcription,
            'seconds': start_time_seconds,
            'transcription_with_seconds' : transcription_with_seconds
        }

        algolia_data.append(algolia_object)

    # Serialize the data to JSON
    algolia_json = json.dumps(algolia_data)

    # Write the Algolia-formatted JSON data to a file or upload it to Algolia index
    with open(f'parsed_jsons/parsed{i}.json', 'w') as json_file:
        json_file.write(algolia_json)


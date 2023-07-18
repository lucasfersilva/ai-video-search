import json
import random
import uuid



json_path = 'parsed_jsons/2023-04-19 12-24-23-KC-Bug8014.json'


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
    unique = uuid.uuid4()
    # Create an Algolia-formatted object
    algolia_object = {
        'objectID': str(unique),
        'video_id': video_id,
        'title': title,
        'labels': label,
        'annotations': annotations,
        'transcription': video_transcription
    }

    algolia_data.append(algolia_object)

# Serialize the data to JSON
algolia_json = json.dumps(algolia_data)

# Write the Algolia-formatted JSON data to a file or upload it to Algolia index
with open('parsed_jsons/reduce_json.json', 'w') as json_file:
    json_file.write(algolia_json)


def parseTranscript(jsonBlob):
    return [
        {
            'text': None,
            'entity': None,
            'transcript': alternative['transcript'],
            'confidence': alternative['confidence'],
            'start_time': alternative['words'][0]['start_time'],
            'words': [
                {
                    'start_time': word['start_time']['seconds'] or 0,
                    'end_time': word['end_time']['seconds'],
                    'word': word['word']
                }
                for word in alternative['words']
            ]
        }
        for annotation in jsonBlob['annotation_results']
        if annotation.get('speech_transcriptions')
        for transcription in annotation['speech_transcriptions']
        if len(transcription['alternatives'][0]) > 0
        for alternative in transcription['alternatives']
    ]


def parseShotLabelAnnotations(jsonBlob):
    return [
        {
            'text': None,
            'transcript': None,
            'entity': annotation['entity']['description'],
            'confidence': segment['confidence'],
            'start_time': segment['segment']['start_time_offset']['seconds'] or 0,
            'end_time': segment['segment']['end_time_offset']['seconds']
        }
        for annotation in jsonBlob['annotation_results']
        if annotation.get('shot_label_annotations')
        for annotation in annotation['shot_label_annotations']
        for segment in annotation['segments']
    ]

def parseTextAnnotations(jsonBlob):
    return [
        {
            'transcript': None,
            'entity': None,
            'text': annotation['text'],
            'confidence': segment['confidence'],
            'start_time': segment['segment']['start_time_offset']['seconds'] or 0,
            'end_time': segment['segment']['end_time_offset']['seconds']
        }
        for annotation in jsonBlob['annotation_results']
        if annotation.get('text_annotations')
        for annotation in annotation['text_annotations']
        for segment in annotation['segments']
    ]

parseTranscript('parsed_json/2022-09-29 19-33-04..json')
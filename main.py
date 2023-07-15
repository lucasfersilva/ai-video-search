from typing import cast

from google.cloud import videointelligence_v1 as vi
from google.cloud import storage

storage_client = storage.Client('BLOB-NAME')
blobs = storage_client.list_blobs('videos_intelligence')


def detect_speech(video_uri: str, output_json) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    language_code = 'en-GB'
    config = vi.SpeechTranscriptionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    context = vi.VideoContext(speech_transcription_config= config)
    features = [vi.Feature.SPEECH_TRANSCRIPTION]
    request = vi.AnnotateVideoRequest(input_uri=video_uri,output_uri=output_json,features=features, video_context = context)

    print(f'Processing video: "{video_uri}"...')
    operation = video_client.annotate_video(request, timeout=3600)

    # Wait for operation to complete
    response = cast(vi.AnnotateVideoResponse, operation.result())
    # A single video is processed
    results = response.annotation_results[0]

    return results


for blob in blobs:
    blob_location = f"gs://{blob.bucket.name}/{blob.name}"
    if blob_location.endswith('.json'):
        continue
    elif blob_location.endswith('.zip'):
        continue
    else:
        try:
            print(blob_location)
            video_uri = blob_location
            json_output = blob_location.replace('.mkv','.json')
            results = detect_speech(video_uri,json_output)
            print(f'{blob.name} was trained')
        except TimeoutError:
            print(f'Video {blob.name} was not trained due to timeout')
            continue

#gs://videos_intelligence/2022-08-22 16-11-31.mkv
#gs://videos_intelligence/2022-08-22 16-11-31.mkv
#gs://videos_intelligence//b/videos_intelligence/o/2022-08-22%2016-11-31.mkv

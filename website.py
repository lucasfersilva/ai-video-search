from flask import Flask, render_template,request, Response
from algoliasearch.search_client import SearchClient
from google.cloud import storage

app = Flask(__name__)

ALGOLIA_APP_ID = '5GGKFNVXJC'
ALGOLIA_API_KEY = '5d2c468dbf811e8dde793c2d4bc2c7dd'
ALGOLIA_INDEX_NAME = 'ai_video_search'

client = SearchClient.create(ALGOLIA_APP_ID,ALGOLIA_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')


def get_video_urls(hit):
    # Replace 'your_bucket_name' with your actual GCS bucket name
    bucket_name = 'videos_intelligence'

    # Assuming that you have a field named 'video_path' in your Algolia index that stores the path of the video in GCS
    video_path = hit.get('video_id')

    if video_path:

        blob = f"https://storage.googleapis.com{video_path}"
        #print(blob)
        if blob is not None:
            return blob

    return None

@app.route('/video/<path:video_path>')
def stream_video(video_path):
    blob = get_video_urls(video_path)

    if not blob.exists():
        return "Video not found", 404

    # Set the appropriate content type for video
    content_type = 'video/mp4'  # Change this according to the video format if needed

    # Create a response to stream the video
    response = Response(blob.download_as_bytes(), mimetype=content_type)
    response.headers['Accept-Ranges'] = 'bytes'
    return response


@app.route('/search', methods=['GET', 'POST'])
def search():
    index = client.init_index(ALGOLIA_INDEX_NAME)

    if request.method == 'POST':
        query = request.form['query']

        results = index.search(query)
        for hit in results['hits']:
            hit['video_id'] = get_video_urls(hit)
            transcription = hit.get('transcription_with_seconds',[])
            for i in transcription:
                if i['transcription']  in query:
                    seconds = i['start_time_seconds']
                    hit['start_seconds'] = seconds
                    print(seconds)
                    continue


        return render_template('results.html', results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8130)
from flask import Flask, render_template,request
from algoliasearch.search_client import SearchClient


app = Flask(__name__)

ALGOLIA_APP_ID = ''
ALGOLIA_API_KEY = ''
ALGOLIA_INDEX_NAME = ''

client = SearchClient.create(ALGOLIA_APP_ID,ALGOLIA_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    index = client.init_index(ALGOLIA_INDEX_NAME)

    if request.method == 'POST':
        query = request.form['query']

        results = index.search(query)
        print(results)

        return render_template('results.html', results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8130)

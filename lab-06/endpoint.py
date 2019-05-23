import flask
from flask import Flask, request
from search import *

app = Flask(__name__, static_url_path='/frontend')

articles_count = 10000
ks = [50, 200, 2000]

dictionaries = {}
articles = {}
lsis = {True: {}, False: {}}

print("Loading article database")
for idf in [True, False]:
    dictionaries[idf], articles[idf] = load_articles(articles_count, idf)
    for k in ks:
        print('{}-{}'.format(idf, k))
        lsis[idf][k] = lsi(articles[idf], k, idf)


@app.route('/')
def hello():
    return flask.send_from_directory('frontend', 'index.html')

@app.route('/search', methods=["POST", "GET"])
def search():
    print(request.form)
    raw_query = request.form.get('q')
    k = int(request.form.get('k')) if request.form.get('k') is not None else 2000
    idf = request.form.get('idf') == 'true' if request.form.get('idf') is not None else False

    if k not in ks:
        return flask.jsonify({"error": "invalid k"})
    query = process_query(dictionaries[idf], raw_query)
    return flask.jsonify(best_n(query, 8, lsis[idf][k]))


if __name__ == '__main__':
    print(get_dump_name('test', 0, 0))
    app.run(debug=True)

import csv
import sys
import nltk
import pickle
import numpy as np
import scipy as scipy
from nltk.corpus import stopwords
from nltk.stem.porter import *

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english')).union(['..', ',', '.', '\'', '"'])
lemmatizer = nltk.stem.WordNetLemmatizer()
stemmer = PorterStemmer()
csv.field_size_limit(sys.maxsize)
file = 'articles.csv'


def save_matrix(name, matrix):
    with open('saved/{}'.format(name), 'wb+') as file:
        pickle.dump(matrix, file)


def load_matrix(name):
    with open('saved/{}'.format(name), 'rb') as file:
        return pickle.load(file)


def get_dump_name(name, k, articles_count):
    return '{}-k_{}-arts_{}.pickle'.format(name, k, articles_count)


def stem(content):
    return [stemmer.stem(lemmatizer.lemmatize(token)) for token in
            [word.lower() for word in tokenizer.tokenize(content) if
             word.lower() not in stop_words and len(word) > 1]]


def make_articles(articles_count):
    dictionary = nltk.FreqDist()
    stemmed_articles = []

    with open(file, 'r') as raw_csv:
        reader = csv.reader(raw_csv)
        next(reader)
        for i, row in enumerate(reader):
            stems = stem(row[9])
            dictionary.update(stems)
            stemmed_articles.append(stems)

            sys.stdout.write("\rStemming: {}/{}".format(i + 1, articles_count))
            if i + 1 >= articles_count:
                break

    words = dict(zip(set([entry[0] for entry in dictionary.most_common()]), range(sys.maxsize)))
    print('\n')
    articles = np.zeros((len(words), articles_count), dtype=float)

    # prepare bag of words
    for no, art in enumerate(stemmed_articles):
        sys.stdout.write("\rMaking bag of words: {}/{}".format(no + 1, articles_count))
        for word in art:
            if words.get(word) is None:
                continue
            articles[words.get(word), no] += 1

    # IDF
    for word_i in range(len(words)):
        articles[word_i, :] *= np.log(articles_count / np.count_nonzero(articles[word_i, :]))

    # normalize
    for art_i in range(articles_count):
        if np.sum(articles[:, art_i]) == 0:
            print("empty article ??? {}".format(art_i))
            continue
        articles[:, art_i] /= np.sum(articles[:, art_i])

    sys.stdout.flush()
    return words, scipy.sparse.csc_matrix(articles, dtype=float)


def load_articles(articles_count=5000):
    articles_dump_name = get_dump_name('articles', 0, articles_count)
    words_dump_name = get_dump_name('words', 0, articles_count)
    try:
        articles = load_matrix(articles_dump_name)
        words = load_matrix(words_dump_name)
        return words, articles
    except FileNotFoundError:
        words, articles = make_articles(articles_count)
        save_matrix(articles_dump_name, articles)
        save_matrix(words_dump_name, words)
        return words, articles


def process_query(words, query='islam'):
    stems = stem(query)
    bag_of_words = np.zeros((len(dictionary), 1))
    for word in stems:
        if dictionary.get(word) is None:
            continue
        bag_of_words[words.get(word)] += 1

    # normalize
    bag_of_words /= np.sum(bag_of_words)
    return bag_of_words


def get_articles(ids):
    articles = []
    with open(file, 'r') as raw_csv:
        reader = csv.reader(raw_csv)
        next(reader)
        for i, row in enumerate(reader):
            if i in ids:
                articles.append((row[2], row[9]))
    return articles


def correlation(articles, query):
    correlations = []
    for art_i in range(articles.shape[1]):
        correlations.append((art_i, np.sum(query.T @ articles[:, art_i])))
    correlations.sort(key=lambda art: art[1], reverse=True)
    return correlations


def lsi(article, k):
    u_name = get_dump_name('svd-u', k, article.shape[1])
    s_name = get_dump_name('svd-s', k, article.shape[1])
    vt_name = get_dump_name('svd-vt', k, article.shape[1])
    try:
        u = load_matrix(u_name)
        s = load_matrix(s_name)
        vt = load_matrix(vt_name)
        return u, s, vt
    except FileNotFoundError:
        u, s, vt = scipy.sparse.linalg.svds(articles, k)
        save_matrix(u_name, u)
        save_matrix(s_name, s)
        save_matrix(vt_name, vt)
        return u, s, vt



if __name__ == '__main__':
    articles_count = 5000
    k = 200

    dictionary, articles = load_articles(articles_count=articles_count)
    query = process_query(dictionary, "islam")

    print("svd")
    u, s, vt = lsi(articles, k)
    matrix = np.diag(s) @ vt
    query = np.diag(1 / s) @ u.T @ query
    print(get_articles([art[0] for art in correlation(matrix, query)[:10]]))

    print(s.shape)
    print("finish")

import csv
import sys
import time

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


def get_dump_name(name, k, articles_count, idf = False):
    return '{}-k_{}-arts_{}{}.pickle'.format(name, k, articles_count, 'idf' if idf else '')


def stem(content):
    return [stemmer.stem(lemmatizer.lemmatize(token)) for token in
            [word.lower() for word in tokenizer.tokenize(content) if
             word.lower() not in stop_words and len(word) > 1]]


def make_articles(articles_count, idf):
    dictionary = nltk.FreqDist()
    stemmed_articles = []

    with open(file, 'r') as raw_csv:
        reader = csv.reader(raw_csv)
        next(reader)
        for i, row in enumerate(reader):
            stems = stem('{} {}'.format(row[2], row[9]))
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
    if idf:
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


def load_articles(articles_count, idf):
    articles_dump_name = get_dump_name('articles', 0, articles_count, idf)
    words_dump_name = get_dump_name('words', 0, articles_count, idf)
    try:
        articles = load_matrix(articles_dump_name)
        words = load_matrix(words_dump_name)
        return words, articles
    except FileNotFoundError:
        words, articles = make_articles(articles_count, idf)
        save_matrix(articles_dump_name, articles)
        save_matrix(words_dump_name, words)
        return words, articles


def process_query(words, query='islam'):
    stems = stem(query)
    bag_of_words = np.zeros((len(words), 1))
    for word in stems:
        if words.get(word) is None:
            continue
        bag_of_words[words.get(word)] += 1

    # normalize
    bag_of_words /= np.sum(bag_of_words)
    return bag_of_words


def get_articles(ids, correlations):
    articles = []
    with open(file, 'r') as raw_csv:
        reader = csv.reader(raw_csv)
        next(reader)
        for i, row in enumerate(reader):
            if i in ids:
                articles.append({"title": row[2], "author": row[4], "content": row[9][:1000], "correlation": correlations[i]})
    return articles


def correlation(articles, query):

    correlations = []
    for art_i in range(articles.shape[1]):
        correlations.append((art_i, np.sum(query.T @ articles[:, art_i])))
    correlations.sort(key=lambda art: art[1], reverse=True)
    return list(map(lambda x: x[0], correlations)), list(map(lambda x: x[1], correlations))

def best_n(query, n, svd):
    stvt, diagut = svd
    query = diagut @ query
    ids, correlations = correlation(stvt, query)
    return get_articles(ids[:n], correlations)

def lsi(articles, k, idf):
    stvt_name = get_dump_name('svd-stvt', k, articles.shape[1], idf)
    diagut_name = get_dump_name('svd-diagut', k, articles.shape[1], idf)
    try:
        stvt = load_matrix(stvt_name)
        diagut = load_matrix(diagut_name)
        return stvt, diagut
    except FileNotFoundError:
        u, s, vt = scipy.sparse.linalg.svds(articles, k)
        stvt = np.diag(s) @ vt
        diagut = np.diag(1/s) @ u.T
        save_matrix(stvt_name, stvt)
        save_matrix(diagut_name, diagut)
        return stvt, diagut


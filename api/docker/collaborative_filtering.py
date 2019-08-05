import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD, evaluate

import warnings; warnings.simplefilter('ignore')

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def collab_filter(md, ratings, links_small, credits, keywords):
    # data pre-processing
    id_map = links_small[['movieId', 'tmdbId']]
    links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
    md = md.drop([19730, 29503, 35587])

    md['id'] = md['id'].astype('int')
    smd = md[md['id'].isin(links_small)]
    #smd.shape

    smd['tagline'] = smd['tagline'].fillna('')
    smd['description'] = smd['overview'] + smd['tagline']
    smd['description'] = smd['description'].fillna('')

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(smd['description'])
    #tfidf_matrix.shape

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim[0]

    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')
    md['id'] = md['id'].astype('int')
    #md.shape

    md = md.merge(credits, on='id')
    md = md.merge(keywords, on='id')

    smd = md[md['id'].isin(links_small)]
    #smd.shape

    smd['cast'] = smd['cast'].apply(literal_eval)
    smd['crew'] = smd['crew'].apply(literal_eval)
    smd['keywords'] = smd['keywords'].apply(literal_eval)
    smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
    smd['crew_size'] = smd['crew'].apply(lambda x: len(x))

    smd['director'] = smd['crew'].apply(get_director)

    smd['cast'] = smd['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)

    smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    smd['cast'] = smd['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    smd['director'] = smd['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
    smd['director'] = smd['director'].apply(lambda x: [x,x, x])
    s = smd.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'keyword'
    s = s.value_counts()
    s[:5]
    s = s[s > 1]

    stemmer = SnowballStemmer('english')
    stemmer.stem('dogs')

    def filter_keywords(x):
        words = []
        for i in x:
            if i in s:
                words.append(i)
        return words

    smd['keywords'] = smd['keywords'].apply(filter_keywords)
    smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
    smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    smd['soup'] = smd['keywords'] + smd['cast'] + smd['director'] + smd['genres']
    smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

    count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    count_matrix = count.fit_transform(smd['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    smd = smd.reset_index()
    titles = smd['title']
    indices = pd.Series(smd.index, index=smd['title'])

    reader = Reader()

    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    data.split(n_folds=5)

    svd = SVD()
    #evaluate(svd, data, measures=['RMSE', 'MAE'])
    
    trainset = data.build_full_trainset()
    svd.train(trainset)

    
    id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
    id_map.columns = ['movieId', 'id']
    id_map = id_map.merge(smd[['title', 'id']], on='id').set_index('title')

    return svd, cosine_sim, id_map, indices
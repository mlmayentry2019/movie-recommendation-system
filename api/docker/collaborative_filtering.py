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

def collab_filter(md, ratings, links_small, credits, keywords,smd):
    # data pre-processing
    id_map = links_small[['movieId', 'tmdbId']]
    links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
    
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

    return svd, id_map
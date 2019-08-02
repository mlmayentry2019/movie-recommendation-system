# Dependencies
import pandas as pd
from flask import Flask, jsonify

# Your API definition
app = Flask(__name__)

@app.route('/top_trend', methods=['GET'])
def topTrend():
    top_rating = df_rating.nlargest(20, ['rating', 'timestamp'])
    top_rating_list = top_rating['movieId'].astype(str).tolist()
    
    df_movie['id'] = df_movie['id'].astype(str)
    top_trend_movies = df_movie[df_movie['id'].isin(top_rating_list)]
    return top_trend_movies.to_json()

if __name__ == '__main__':
    df_rating = pd.read_csv('./data/ratings_small.csv')
    df_movie = pd.read_csv('./data/movies_metadata.csv')
    app.run(debug=True, host='0.0.0.0')
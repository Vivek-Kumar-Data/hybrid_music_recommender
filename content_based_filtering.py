import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from category_encoders.count import CountEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from data_cleaning import data_content_based
from scipy.sparse import save_npz

# cleaned data path
cleaned_data_path = 'data/cleaned_data.csv'

# mentioning the columns to transform
frequency_encode_cols = ['year']
ohe_cols = ['artist',"time_signature","key"]
tfidf_col = 'tags'
standard_scale_cols = ["duration_ms","loudness","tempo"]
min_max_scale_cols = ["danceability","energy","speechiness","acousticness","instrumentalness","liveness","valence"]

# transform the respective columns
def train_transformer(data):

    # using column transformer
    transformer = ColumnTransformer(transformers=[
    ("frequency_encode", CountEncoder(normalize=True,return_df=True), frequency_encode_cols),
    ("ohe", OneHotEncoder(handle_unknown="ignore"), ohe_cols),
    ("tfidf", TfidfVectorizer(max_features=85), tfidf_col),
    ("standard_scale", StandardScaler(), standard_scale_cols),
    ("min_max_scale", MinMaxScaler(), min_max_scale_cols)
    ],remainder='passthrough',n_jobs=-1,force_int_remainder_cols=False)

    # fit the data
    transformer.fit(data)
    
    #saving the transformer 
    joblib.dump(transformer,"transformer.joblib")

# function for saving the sparse data
def save_transformed_data(transformed_data,save_path):

    # saving sparse data
    save_npz(save_path,transformed_data)

def transform_data(data):
    
    # load the transformer
    transformer = joblib.load("transformer.joblib")
    
    # transform the data
    transformed_data = transformer.transform(data)
    
    return transformed_data

# function for calculating the cosine similarity
def cosine_similarity(input_vector,data):

    #calculate similarity scores
    similarity_scores = cosine_similarity(input_vector,data)

    return similarity_scores

def content_recommendation(song_name,artist_name,songs_data, transformed_data, k=10):
    
    # convert song name to lowercase
    song_name = song_name.lower()
    # convert the artist name to lowercase
    artist_name = artist_name.lower()
    # filter out the song from data
    song_row = songs_data.loc[(songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)]
    # get the index of song
    song_index = song_row.index[0]
    # generate the input vector
    input_vector = transformed_data[song_index].reshape(1,-1)
    # calculate similarity scores
    similarity_scores = cosine_similarity(input_vector, transformed_data)
    # get the top k songs
    top_k_songs_indexes = np.argsort(similarity_scores.ravel())[-k-1:][::-1]
    # get the top k songs names
    top_k_songs_names = songs_data.iloc[top_k_songs_indexes]
    # print the top k songs
    top_k_list = top_k_songs_names[['name','artist','spotify_preview_url']].reset_index(drop=True)
    # returning top recommendations
    return top_k_list

def main(data_path):
    
    # load the data
    data = pd.read_csv(data_path)
    # clean the data
    data_content_filtering = data_content_based(data)
    # train the transformer
    train_transformer(data_content_filtering)
    # transform the data
    transformed_data = transform_data(data_content_filtering)
    #save transformed data
    save_transformed_data(transformed_data,"data/transformed_data.npz")
    
if __name__ == "__main__":
    main(cleaned_data_path)
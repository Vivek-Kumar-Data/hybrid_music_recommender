# importing necessary libraries
import pandas as pd
import numpy as np

# reading the data path
data_path = 'data/Music Info.csv'

def clean_data(data):
    # droping duplicated values
    data.drop_duplicates(subset="spotify_id",inplace=True)

    # dropping unwanted columns
    data.drop(columns=['genre','spotify_id'],inplace=True)

    # Filling up the missing values in 'tags' column with "No tags"
    data.fillna({"tags":"no_tags"},inplace=True)

    # converting upper case into lower case and resetting the index
    return data.assign(
        name=lambda x : x['name'].str.lower(),
        artist = lambda x : x['artist'].str.lower(),
        tags = lambda x : x['tags'].str.lower()
    ).reset_index(drop=True)

def data_content_based(data):

    # dropping the unwanted columns
    data.drop(columns=['track_id','name','spotify_preview_url'],inplace=True)

    return data

def main(data_path):

    # laoding data
    data = pd.read_csv(data_path)

    # cleaning the data
    cleaned_data = clean_data(data)

    # saving the cleaned data
    cleaned_data.to_csv('data/cleaned_data.csv',index=False)

if __name__ == "__main__":
    main(data_path=data_path)

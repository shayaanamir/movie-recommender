import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests

data = pd.read_csv('final_data.csv')
cv = CountVectorizer()
vector = cv.fit_transform(data['comb'])
similarity = cosine_similarity(vector)

def recommendMovies(movie):
    movie = movie.lower()
    if movie not in data['movie_title'].unique():
        print("Movie not found!")
    else:
        index = data[data['movie_title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:11]:
            print(data.iloc[i[0]]['movie_title'])


recommendMovies('the avengers')
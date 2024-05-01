import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import requests
import json
import os


def preprocess():
    #getting data from URL
    url = 'https://drive.google.com/file/d/1MLilN3ArTUBx-fEzIZF8SjaMyqa8mr8p/view?usp=drive_link'

    # Set path for the input
    RAW_DATA_DIR = os.environ["RAW_DATA_DIR"]
    #RAW_DATA_FILE = os.environ["RAW_DATA_FILE"]
    #RAW_DATA_DIR= '.\cicd\\raw_data'
    #RAW_DATA_FILE='raw_data.csv'
    #raw_data_path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)


    # Read dataset
    raw_data = pd.read_csv('https://drive.usercontent.google.com/download?id={}&export=download&authuser=0&confirm=t'.format(url.split('/')[-2]))

    # Split into train and test
    train, test = train_test_split(raw_data, test_size=0.3, stratify=raw_data['target'])
    #test.drop('target',inplace =True,axis= 1)

    # Set path to the outputs
    PROCESSED_DATA_DIR = os.environ["PROCESSED_DATA_DIR"]
    #PROCESSED_DATA_DIR= '.\cicd\\processed_data'
    train_path = os.path.join(PROCESSED_DATA_DIR, 'train.csv')
    test_path = os.path.join(PROCESSED_DATA_DIR, 'test.csv')

    # Save csv
    train.to_csv(train_path, index=False)
    test.to_csv(test_path,  index=False)
    print('Preprocessing finished')
   


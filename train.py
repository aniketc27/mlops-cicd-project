import pandas as pd
import numpy as np
from joblib import dump
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, roc_curve, auc
import lightgbm as lgb
import xgboost as xgb
import pickle
import json
import os

def train():
    # Set path to inputs
    PROCESSED_DATA_DIR = os.environ["PROCESSED_DATA_DIR"]
    #PROCESSED_DATA_DIR = '.\cicd\\processed_data'
    train_data_file = 'train.csv'
    train_data_path = os.path.join(PROCESSED_DATA_DIR, train_data_file)

    # Read data
    data = pd.read_csv(train_data_path, sep=",")

    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    features = [c for c in data.columns if c not in ["ID_code", "target"]]
    target = data["target"]

    param = {
        'bagging_freq': 5,
        'bagging_fraction': 0.4,
        'boost_from_average':'false',
        'boost': 'gbdt',
        'feature_fraction': 0.05,
        'learning_rate': 0.01,
        'max_depth': -1,  
        'metric':'auc',
        'min_data_in_leaf': 80,
        'min_sum_hessian_in_leaf': 10.0,
        'num_leaves': 13,
        'num_threads': 8,
        'tree_learner': 'serial',
        'objective': 'binary', 
        'verbosity': 1
    }

    of = np.zeros(len(data))

    # Generate train and validation set indices to iterate on train values and target values.
    for counter_, (trn_idx, val_idx) in enumerate(folds.split(data.values, target.values)):
        print("Fold {}".format(counter_))
        
        train = lgb.Dataset(data.iloc[trn_idx][features], label=target.iloc[trn_idx])
        val = lgb.Dataset(data.iloc[val_idx][features], label=target.iloc[val_idx])
        
        #model classifier
        classifier = lgb.train(param, train, 1000000, valid_sets = [train, val],callbacks=[lgb.early_stopping(stopping_rounds=80), lgb.log_evaluation(50)])
        
        of[val_idx] = classifier.predict(data.iloc[val_idx][features], num_iteration=classifier.best_iteration)

    # Set path to output (model)
    MODEL_DIR = os.environ["MODEL_DIR"]
    #MODEL_DIR = '.\cicd\\model'
    model_name = 'lightGBM_model.joblib'
    model_path = os.path.join(MODEL_DIR, model_name)

    # Serialize and save model
    dump(classifier, model_path)
    print('Training finished')
    
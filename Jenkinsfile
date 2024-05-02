
pipeline {
    agent 
    {
    docker { image 'jupyter/scipy-notebook' }
    }

    environment {
        MODEL_DIR='./model'
        PROCESSED_DATA_DIR='./processed_data'
        RESULTS_DIR='./results'
    }
    stages {
        stage('install dependencies') {
        steps {
            sh 'python -m pip install joblib xgboost lightgbm flask'
        }
        }
        
        stage('Preprocess') {
            steps {
                echo 'Preprocessing'
                sh 'python3 preprocess.py'
            }
        }
        stage('Train') {
            steps {
                echo 'Training'
                sh 'python3 train.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
                sh 'python3 testing.py'
            }
        }
    }
}

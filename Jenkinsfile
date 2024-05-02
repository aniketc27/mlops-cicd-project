
pipeline {

    agent any

    environment {
        MODEL_DIR='./model'
        PROCESSED_DATA_DIR='./processed_data'
        RESULTS_DIR='./results'
    }
    stages {

        stage('install dependencies') {
        steps {
            bat 'python -m pip install -r requirements.txt'
        }
        }
        
        stage('Preprocess') {
            steps {
                echo 'Preprocessing'
                bat 'python3 preprocess.py'
            }
        }
        stage('Train') {
            steps {
                echo 'Training'
                bat 'python3 train.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
                bat 'python3 testing.py'
            }
        }
    }
}

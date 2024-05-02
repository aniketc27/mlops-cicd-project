
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
            sh 'python -m pip install -r requirements.txt'
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

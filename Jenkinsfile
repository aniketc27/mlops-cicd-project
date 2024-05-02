
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
            echo 'Installing dependencies'
            withPythonEnv('python3'){bat 'python3 -m pip install -r requirements.txt'}
        }
        }
        
        stage('Preprocess') {
            steps {
                echo 'Preprocessing'
                withPythonEnv('python3'){bat 'python3 preprocess.py'}
            }
        }
        stage('Train') {
            steps {
                echo 'Training'
                withPythonEnv('python3'){bat 'python3 train.py'}
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
                withPythonEnv('python3'){bat 'python3 testing.py'}
            }
        }
        
    }
}

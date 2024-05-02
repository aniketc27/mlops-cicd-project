pipeline {
    agent any

    environment {
        MODEL_DIR = './model'
        PROCESSED_DATA_DIR = './processed_data'
        RESULTS_DIR = './results'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 -m pip install -r requirements.txt' || error 'Failed to install dependencies'
                    }
                }
            }
        }

        stage('Preprocess') {
            steps {
                echo 'Preprocessing'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 preprocess.py' || error 'Preprocessing failed'
                    }
                }
            }
        }

        stage('Train') {
            steps {
                echo 'Training'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 train.py' || error 'Training failed'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Testing'
                script {
                    withPythonEnv('python3') {
                        sh 'python3 testing.py' || error 'Testing failed'
                    }
                }
            }
        }
    }

}

#!/usr/bin/env groovy
pipeline {
    agent any

    stages {
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

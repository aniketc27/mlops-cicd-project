#!/usr/bin/env groovy
pipeline {

    agent any

    stages {
        
        stage('Clone repository')
        {
        /* Let's make sure we have the repository cloned to our workspace */
            steps{
                checkout scm
                echo 'Git'
            }
        
        }
        
        stage('Docker Build') {
            steps {
                echo 'Building'
                script {
                    /* Docker build step */
                    app = docker.build("lightmodel")
                }
            }
        }

        stage('Docker Run') {
            steps {
                echo 'Running'
                //sh 'docker run -p 5001:5001 lightmodel'
                script {
                    /* Docker run step */
                    // app = docker.build("lightmodel")
                    docker.image('lightmodel').run('-p 5001:5001')
                }
            }
        }
        
    }
}
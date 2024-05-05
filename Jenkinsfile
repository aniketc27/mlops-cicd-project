#!/usr/bin/env groovy
pipeline {

    agent any
    
    environment {
        //API version
        APP_VERSION = "1.0.0"
        //Model version
        MODEL_VERSION = "1.0.0"
    }

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
                    image_name = "light-model-${env.APP_VERSION}-${env.MODEL_VERSION}"
                    app = docker.build(image_name)
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
                    docker.image(image_name).run('-p 5001:5001')
                }
            }
        }
        
    }
}
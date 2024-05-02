pipeline {

    agent any

    environment {
        MODEL_DIR='./model'
        PROCESSED_DATA_DIR='./processed_data'
        RESULTS_DIR='./results'
        
    }
    stages {
        
        stage('Clone repository')
        {
        /* Let's make sure we have the repository cloned to our workspace */
            steps{
                checkout scm
            }
        
        }
        
        stage('Docker Build') {
            steps {
                echo 'Building'
                docker.build("lightmodel")
            }
        }
        
    }
}

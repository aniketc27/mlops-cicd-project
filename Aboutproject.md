# MLOps CI/CD Project

## Overview

This project showcases the development and deployment of a Machine Learning Operations (MLOps) pipeline using a combination of open-source tools and cloud services. Challenges were encountered and resolved throughout the project, with a focus on efficient data management, model development, and pipeline automation.

## Tools Used

- **Data Management:** Google Drive
- **Model Development:** LightGBM, mlflow
- **Pipeline Tools:** GitHub, Jenkins, Docker, Flask, Azure App Service

## Project Workflow

### 1. Data Acquisition

Acquiring data is a fundamental step in any machine learning project. To maintain best practices and avoid storing large datasets within the code repository, the dataset was hosted on Google Drive. Access to the data was provided via a shared link with appropriate permissions. This approach ensures data integrity and minimizes the repository's size.

### 2. Model Development

Model development involved selecting an appropriate algorithm and tuning its hyperparameters. In this project, LightGBM, a gradient boosting framework, was chosen for its efficiency and performance. To track experiments and model metrics, mlflow was employed. This facilitated the comparison of different model iterations and parameter configurations.

An important consideration during model development was the interpretation of feature importance. To address this, metadata, including feature importance scores, was stored alongside the model artifacts. This practice enhances model explainability and aids in feature selection or debugging.

### 3. Pipeline Design

#### Initial Plan:
The initial pipeline design aimed to streamline the workflow by separating distinct stages into individual Python scripts. These stages included data preprocessing, model training, and testing. Jenkins, a continuous integration and continuous delivery (CI/CD) tool, was utilized to automate pipeline execution.

#### Final Solution:
However, due to challenges encountered in configuring Jenkins and managing dependencies, a revised approach was adopted. A unified `run.py` script was developed to orchestrate the entire pipeline. This script facilitated easier containerization using Docker, which ensured consistent environments across different stages of the pipeline.

Additionally, to deploy the Flask app and expose the model predictions publicly, Azure App Service was chosen. This cloud service offers scalability and reliability, making it suitable for hosting web applications. By leveraging Azure App Service's free tier, the project achieved cost-effectiveness while ensuring accessibility.

## Pipeline Steps

1. **Data Preprocessing**: 
   - The `preprocess.py` script retrieves raw data from Google Drive, performs necessary preprocessing, and generates train and test datasets. This step ensures data readiness for model training and testing.

2. **Model Training**:
   - The `train.py` script trains the LightGBM model using the prepared datasets and stores the trained model as a joblib file. Hyperparameter tuning is performed to optimize model performance and reduce training time.

3. **Model Testing**:
   - The `test.py` script evaluates the trained model's performance using the test dataset. Model metrics are computed and stored for analysis and comparison.

4. **Pipeline Execution**:
   - The `run.py` script orchestrates the entire pipeline by sequentially executing the preprocessing, training, and testing scripts. This ensures a consistent and reproducible workflow.

5. **Deployment**:
   - The `app.py` script loads the trained model and exposes endpoints for making predictions via a Flask web application. This application is deployed on Azure App Service, making the predictions publicly accessible.

## How to Run

1. **Clone the Repository**:
git clone <repository-url>
cd mlops-cicd-project


2. **Build and Run Docker Container**:
docker build -t light-model .
docker run -p 5001:5001 light-model


3. **Access the Flask App**:
- Once the Docker container is running, use Postman or a web browser to send file requests to `[link]/predict`, where `[link]` is the URL provided by Azure App Service. Ensure that debug mode is set to True for debugging purposes.

**Note:** Before running the Docker commands, ensure that no existing Docker container with the same name is running to avoid conflicts.

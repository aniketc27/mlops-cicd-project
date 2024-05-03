# MLOps CI/CD Project

## Overview

This project showcases the development and deployment of a Machine Learning Operations (MLOps) pipeline using a combination of open-source tools and cloud services. Challenges were encountered and resolved throughout the project, with a focus on efficient data management, model development, and pipeline automation.

## Tools Used

- **Data Management:** Google Drive , pandas
- **Model Development:** LightGBM, mlflow , joblib 
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


# My views and thoughts on the project

It was fun working on this project I did face several challenges and changed approaches while working on it. Was able to resolve them and complete this project.Designing and implementing it with free open source services was a challenge as I ran into several issues which we generally do not face in cloud native environment .I appreciate cloud architecture more for the seamless abstractions it provides.

**Lets start from beginning** 

1. Getting Data 
It was a open Kaggle Dataset. And it is not a good practise to keep data in your code repo thus I uploaded in google drive and made the data csv files accessible via link and set the permissions accordingly. Added necessary code in my notebooks and py scripts to fetch data directly.

2. Model Development  
Model development was interesting and there wasn't enough context in the column names/headers to draw conclusions. Considering the scenario I chose LightGBM model and did the training over 10 folds, was getting high accuracy and auc scores of greater than 0.9 with training and ~0.9 in validation set. Under the model-development folder you will see mlruns/0 where you can see previous runs as I was using mlflow to track each experiment while storing the model artifacts,inputs,metrics,params and meta.yaml.

Under the model subfolder stored all the metadata,python_env.yaml and requirements.txt,also added storing feature_importance_gain.json and png file for reference to check them during development phase, the modeling logic changes often.Took consideration of data KPIs as they to change and we begin using a different features to train and test the model. I stored the metrics for easier comparision among different models/modeling logics.

An important step here was tuning the hyper params properly as initial run of the model took almost 4 hours,fine tuned the hyper parameters and resulting in complete training in sub 25 mins considering the size of data and my pc's specification.The params stored helped achieve it.

3. Pipeline design 
Pushed all the code in github repo which is used for further ci/cd/ct. Used Jenkins for ci/cd/ct triggering a docker build to containerize the flask app which can be used to api requests with a csv file to do model predictions returned as a json output. An important step which took me sometime to configure was making Github webhook, github used to support http but it does not anymore I had to use ip tunneling ,used ngrok to accomplish it and set the github hook for all push events which triggers a Jenkins pipeline build.

**More about Pipeline steps (spent the most time and delayed my project completion)**

About files

preprocess.py ==> gets raw data from source(google drive) does a bit preprocessing and makes train.csv and test.csv
train.py ==> trains model stores in joblib file
test.py ==> tests the trained model stores the results 
run.py ==> executes all the above scripts
app.py ==> flask app which loads the model and can take csv files to make predictions

**Initial plan:**

Use the three python scripts preprocess.py , train.py , testing.py run as individual stages and save outputs in docker container enables us save compute costs as offloads it in pipeline runs (in my experience working in Azure it is always cheaper to run your incremental builds over pipelines than over computes)rather than workspace.Continue to deploy the flask app and final model files used to predict.  I failed with this approach even after creating the correct jenkins file running into issues (had to increase ram as it was an intensive load for my pc to run and corrupted windows in the process resulting in starting from ground 0) ,following errors related to path variables which prevented my Jenkins localhost from accessing and running python commands.I could not resolve it over multiple different pipeline builds(approx ~30) and several reruns.

**Final solution:**

Created a run.py script and decided to containerize the build in a docker container ,with every code push which occurs in github repo triggering a pipeline build. It creates a docker image and subsequently make a docker container with an exposed port. I chose 5001 port as local 5000 port was partially occupied and ran into problems while trying to communicate . Have the app.py take the latest generated model file and deploy it. Used Azure cloud app-service free tier to make the flask app publicly available at the url https://app-cls.azurewebsites.net/ (as it is a free tier I have for the time being shut it off to save credits). I did try other approaches of ip tunneling for https forwarding ngrok has a one port forwarding per sign-up-ip policy so could not use it,other ip-tunnelling options had major issue while sending the csv files causing 400 request errors and 502 bad request errors. Settled with Azure App Service to deploy the flask app over the web. (You get 200 free credits to play around seemed like a good call for the MVP).

**Solution Explanation:**

1. On push to the github repo, a jenkins pipeline is triggered automatically using github hook.
2. Jenkins file builds a docker image and runs a container
3. The python scripts invoked and run.py which calls the preprocess.py to create train and test csvs from raw data and do some preprocessing.Justification in development scenarios if KPIs or source of data is changed the preprocess pipeline requires to updated accordingly and create correct datasets on which training will commence. The csv files are stored in processed_data directory.run.py then calls train.py which trains the model and stores the model as a joblib file under model directory as joblib file. Justification modelling logic can change or hyper parameter tuning can be changed.Finally testing.py which loads the saved model and tests on a test csv from proccesed_data directory and stores results.
4. The joblib model file is then called in app.py which can take a csv file input (used postman to validate it) and provides output via exposed ports outside of docker container as a json.
5. Have deployed the flask app in azure app services with which it can be called publicly





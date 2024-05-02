# mlops-cicd-project
Tools used:-

It was fun and sometimes not so fun while working on this project I faced several problems changes approaches shifted things from here and there, had a very messy code. Well finally I was able to resolve most of them and complete this project.Making it with completely free open source services is extremely hard and I ran into several issues which we generally do not face in cloud native environment to be honest I now appreciate cloud solutions more than before.

Lets start from the very start

1. Getting Data 
So it was a open Kaggle Dataset. And it is never a good practise to keep data in your code repo so I uploaded in google drive where I made the data csv files accessible via link and set the permissions accordingly. Added code in my notebooks and py scripts to fetch from it directly.

2. Model Development  
Well model development was interesting and there was not much context provided in the column names from which we could draw conclusions considering the scenario I chose LightGBM model and I did the training over 10 folds I was getting very high accuracy and auc scores of greater than 0.9 with training and ~0.9 in validation set. Under the model-development folder you will see mlruns > 0 where you can see around 10/12 runs as I was using mlflow to track each experiment I was storing the model artifacts,inputs,metrics,params and meta.yaml.
Under the model subfolder I am storing all the metadata,python_env.yaml and requirements.txt, I was also storing feature_importance_gain.json and png file for reference to check them as during development phase modeling logic changes often. I took into account of data as there are several times when KPIs are changed and we start using a different features to train and test the model. I stored the metrics for easier comparision among different models.

An important step here was tuning the hyper params properly as initial run of the model took almost 4 hours I fine tuned the hyper parameters and now it does complete training in sub 25 mins which was still really good considering the size of data and my laptop's configuration.The params helped to do it.

3. Pipeline design 
I pushed all the code in github repo which will be used for further ci/cd/ct. I have used Jenkins for ci/cd/ct which triggers a docker build to containerize the flask app which can be used to send requests as a csv file and you wil get a json output. A very important place which took me sometime to configure making Github webhook, github used to support http but it does not anymore I had to ip tunneling , I used ngrok to accomplish it and set the github hook for all push events which triggers a Jenkins pipeline build.

More about Pipeline steps this is where I spent the most time and delayed my project completion. 

About files
preprocess.py ==> gets raw data from source(google drive again) does a bit preprocessing and makes train.csv and test.csv
train.py ==> trains model stores in joblib file
test.py ==> tests the trained model stores the results 
run.py ==> executes all the above scripts
app.py ==> flask app which loads the model and can take csv files to make predictions

Initial plan:

Have the three python scripts preprocess.py , train.py , testing.py run in individual stages and save outputs in docker container this helps with saving compute and offloads it in pipeline runs from experience in working in Azure it is always cheaper to run your incremental builds over pipelines than over computes in your workspace. I failed with this approach I did create the correct jenkins file but due to some issues (had to upgrade my laptops ram as it was an intensive load for it to run I corrupted my windows and had to redo things from the start) then later I did run into some path variables which prevented my Jenkins from being able to run python and I could not resolve it even after 30 different pipeline builds and several retries.

Final solution:

Created a run.py script and decided to containerize the builds in a docker container so every time there is a code change which occurs in github repo a pipeline build is triggered. Which creates a docker image and used to make a docker container with an exposed port. I chose 5001 port as local 5000 port was always occupied and ran into some problems while trying to communicate with outside of the docker container. Have the app.py take the latest generated model and deploy it over web. Used Azure cloud app-service free tier to make the app publicly available at the url https://app-cls.azurewebsites.net/ (as it is a free tier I have for the time being shut it off). I tried other approaches of trying to ip tunneling again the exposed port but ngrok has a one port forwarding per sign-up-ip policy so could not use it. Tried other ip-tunnelling options the major issue which I faced there was sending the csv files which was resulted in 400 errors and 502 errors. Settled with Azure App Service for the same. (You get free 200 credits to play around so for the MVP I presumed it to be a good call).

Solution Explanation :

1. On push to the github repo a jenkins pipeline is triggered automatically.
2. Jenkins file builds a docker image and runs a container
3. The python scripts invoked and run.py which calls the preprocess.py to create train and test csvs and do some preprocessing.Justification in development scenarios if KPIs or source of data is changed this preprocess pipeline requires to changed and accordingly create correct datasets on which training will commence. The csv files are stored in preprocessed directory. The run.py then triggers train.py which trains the model and stores the model as a joblib file under model directory. Finally testing.py which loads the saved model and tests over a test csv from preproccesed directory and stores results.
4. The joblib file is then called in app.py which can take a file input of csv (used postman to validate it) and gives outputs via exposed ports outside of docker container as a json.
5. Have deployed the flask app in azure app services with which it can be called publicly

How to run:

1. Clone the repository
2. You can run the dockerfile to create the image and container 
commands 
docker build -t light-model .
docker run -p 5001:5001 light-model
3. app.py is already running so use postman to send files requests on [link]/predict

PS if you have an image with same name running already please delete it before running the commands again as it will cause issues




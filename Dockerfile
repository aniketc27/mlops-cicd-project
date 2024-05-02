FROM jupyter/scipy-notebook
USER root
RUN apt-get update && apt-get install -y jq
USER root

RUN pip install joblib
RUN pip install xgboost
RUN pip install lightgbm
RUN pip install flask
RUN mkdir model processed_data results

ENV MODEL_DIR=/home/jovyan/model
ENV PROCESSED_DATA_DIR=/home/jovyan/processed_data
ENV RESULTS_DIR=/home/jovyan/results
#ENV MODEL_FILE=light_model.joblib

COPY light_model.joblib ./model/light_model.joblib
COPY preprocess.py ./preprocess.py
COPY train.py ./train.py 
COPY testing.py ./testing.py
COPY run.py ./run.py
COPY app.py ./app.py

RUN python3 run.py
EXPOSE 5001
#docker run -p 5001:5001 light-model

#CMD [ "python3", "run.py" ]
CMD [ "python3", "app.py" ]
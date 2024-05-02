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

COPY preprocess.py ./preprocess.py
COPY train.py ./train.py
COPY testing.py ./testing.py
COPY run.py ./run.py
COPY app.py ./app.py

EXPOSE 5000

CMD [ "python3", "run.py" ]
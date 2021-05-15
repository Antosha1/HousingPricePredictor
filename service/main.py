from fastapi import FastAPI, status, HTTPException, Request, Response, Depends
from pydantic import BaseModel
import redis
import hiredis
import json
from datetime import datetime


app = FastAPI()


def decode_none(s):
    if s is None:
        return None
    if isinstance(s, dict):
        return {decode_none(k): decode_none(v) for k, v in s.items()}
    if isinstance(s, list):
        return [decode_none(k) for k in s]
    if isinstance(s, bytes):
        return s.decode(encoding='utf-8')
    return str(s)


def encode_none(s):
    if s is None:
        return None
    if isinstance(s, dict):
        return {encode_none(k): decode_none(v) for k, v in s.items()}
    if isinstance(s, list):
        return [encode_none(k) for k in s]

    return bytes(str(s), encoding='utf-8')


def state_function(func):
    class CustomStr(str):
        def __call__(self):
            return func.__name__, str(datetime.now())

    return CustomStr(func.__name__)


class Dataset:
    """
    Datasets are stored in in Redis KV storage

    #state markers
    created: str
    deleted: str
    """

    @staticmethod
    @state_function
    def created():
        ...


class Model:
    """
    Machine Learning models are stored in Redis KV storage

    #state markers
    created: str
    deleted: str
    """

    @staticmethod
    @state_function
    def created():
        ...

    @staticmethod
    @state_function
    def trained():
        ...


class Prediction:
    """
    Predictions are stored in Redis KV storage

    #state markers
    created: str
    deleted: str
    """

    @staticmethod
    @state_function
    def created():
        ...


@app.get('/models/')
def get_models(response: Response):
    pass


@app.get('/models/{model_id}/')
def get_model():
    pass


@app.post('/models/{dataset_id}')
def add_model():
    pass


@app.get('/dataset/')
def get_datasets(response: Response):
    pass


@app.get('/dataset/{dataset_id}')
def get_dataset_info():
    pass


@app.get('/dataset/{dataset_id}/data')
def get_dataset_data():
    pass


@app.post('/dataset/')
def add_dataset():
    pass


@app.get('/predict/')
def get_predictions(response: Response):
    pass


@app.get('/predict/{pred_id}/models/{model_id}/dataset/{dataset_id}/data')
def get_prediction():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

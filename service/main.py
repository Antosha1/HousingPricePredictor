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
    def dataset_key(date):
        return f"dataset:d{'_'.join(str(date).split())}"

    @staticmethod
    def dataset_hash(dataset_id):
        return f"/dataset/{dataset_id}"

    @staticmethod
    def datasets():
        return "/datasets"

    @staticmethod
    @state_function
    def created():
        ...

    @staticmethod
    def to_db(**kwargs):
        return dict(
            description=encode_none(kwargs.get("description", None)),
            data=encode_none(kwargs.get("data", None)),
            date=encode_none(kwargs["date"])
        )

    @staticmethod
    def from_db(**kwargs):
        return dict(
            description=decode_none(kwargs.get("description", None)),
            data=decode_none(kwargs.get("data", None)),
            date=decode_none(kwargs["date"]),
            created=decode_none(kwargs["created"])
        )


class AddDataset(BaseModel):
    description: str
    data: str
    date: str


class GetDatasetOut(BaseModel):
    description: str
    data: str
    date: str
    created: str


class Model:
    """
    Machine Learning models are stored in Redis KV storage

    #state markers
    created: str
    deleted: str
    """

    @staticmethod
    def model_key(date):
        return f"model:d{'_'.join(str(date).split())}"

    @staticmethod
    def model_hash(model_id):
        return f"/model/{model_id}"

    @staticmethod
    def models():
        return "/models"

    @staticmethod
    @state_function
    def created():
        ...

    @staticmethod
    @state_function
    def trained():
        ...

    @staticmethod
    def to_db(**kwargs):
        return dict(
            description=encode_none(kwargs.get("description", None)),
            metadata=encode_none(kwargs.get("metadata", None)),
            date=encode_none(kwargs["date"])
        )

    @staticmethod
    def from_db(**kwargs):
        return dict(
            description=decode_none(kwargs.get("description", None)),
            metadata=encode_none(kwargs.get("metadata", None)),
            date=decode_none(kwargs["date"]),
            created=decode_none(kwargs["created"]),
            trained=decode_none(kwargs["trained"])
        )


class AddModel(BaseModel):
    description: str
    metadata: str
    date: str


class GetModelOut(BaseModel):
    description: str
    metadata: str
    date: str
    created: str
    trained: str


class RequestModel:
    """
    Requests are stored in Redis KV storage

    #state markers
    created: str
    """
    @staticmethod
    def request_key(date):
        return f"request:d{'_'.join(str(date).split())}"

    @staticmethod
    def request_hash(req_id):
        return f"/request/{req_id}"

    @staticmethod
    @state_function
    def created():
        ...

    @staticmethod
    def to_db(**kwargs):
        return dict(
            model_id=encode_none(kwargs.get("model_id", None)),
            dataset_id=encode_none(kwargs.get("dataset_id", None)),
            response=encode_none(kwargs.get("response", None))
        )

    @staticmethod
    def from_db(**kwargs):
        return dict(
            model_id=decode_none(kwargs.get("model_id", None)),
            dataset_id=decode_none(kwargs.get("dataset_id")),
            response=encode_none(kwargs.get("response", None)),
            created=decode_none(kwargs["created"])
        )


class AddRequest(BaseModel):
    model_id: str
    dataset_id: str
    response: str


class GetRequestOut(BaseModel):
    model_id: str
    dataset_id: str
    response: str
    created: str


# @app.route('/')
# def greetings():
#     return "Welcome to House Price Predictor web-service!"


@app.get('/models/')
def get_models(response: Response):
    r = redis.Redis()

    result = []
    for p in r.smembers(Model.models()):
        result.append(
            dict(
                model_id=decode_none(p),
                url=f"{Model.model_hash(decode_none(p))}/"
            )
        )

    response.status_code = status.HTTP_200_OK
    return result


@app.post("/models/",
          responses={201: {"description": "Model was added"}})
def add_model(model: AddModel,
              response: Response):
    r = redis.Redis()
    model_key = Model.model_key(model.date)
    model_hash = Model.model_hash(model_key)

    with r.pipeline() as pipe:
        try:
            pipe.watch(model_hash)

            res = pipe.hsetnx(model_hash, *Model.created())
            if res == 1:
                pipe.hset(model_hash, mapping=Model.to_db(
                    description=model.description,
                    metadata=model.metadata,
                    date=model.date
                ))

                pipe.sadd(Model.models(), model_key)

                response.status_code = status.HTTP_201_CREATED

                model_url = f"{model_hash}/"
                response.headers["Location"] = model_url
                return

            response.status_code = status.HTTP_409_CONFLICT
            return

        except redis.WatchError:
            response.status_code = status.HTTP_409_CONFLICT
            return


@app.get("/models/last/")
def get_last_model(response: Response):
    r = redis.Redis()
    result = r.rpop(Model.models())

    response.status_code = status.HTTP_200_OK
    return result


@app.get("/models/{model_id}/", response_model=GetModelOut)
def get_model(model_id,
              response: Response):
    r = redis.Redis()
    model_hash = Model.model_hash(model_id)
    res = r.hgetall(model_hash)
    if len(res) > 0:
        res = Model.from_db(**decode_none(res))

        response.status_code = status.HTTP_200_OK
        return GetModelOut(**res)

    response.status_code = status.HTTP_404_NOT_FOUND
    return None


@app.get("/dataset/")
def get_datasets(response: Response):
    r = redis.Redis()

    result = []
    for p in r.smembers(Dataset.datasets()):
        result.append(
            dict(
                dataset_id=decode_none(p),
                url=f"{Dataset.dataset_hash(decode_none(p))}/"
            )
        )

    response.status_code = status.HTTP_200_OK
    return result


@app.post("/dataset/",
          responses={201: {"description": "Dataset was added"}})
def add_dataset(dataset: AddDataset,
                response: Response):
    r = redis.Redis()
    dataset_key = Dataset.dataset_key(dataset.date)
    dataset_hash = Dataset.dataset_hash(dataset_key)

    with r.pipeline() as pipe:
        try:
            pipe.watch(dataset_hash)

            res = pipe.hsetnx(dataset_hash, *Dataset.created())
            if res == 1:
                pipe.hset(dataset_hash, mapping=Dataset.to_db(
                    description=dataset.description,
                    data=dataset.data,
                    date=dataset.date
                ))

                pipe.sadd(Dataset.datasets(), dataset_key)

                response.status_code = status.HTTP_201_CREATED

                dataset_url = f"{dataset_hash}/"
                response.headers["Location"] = dataset_url
                return

            response.status_code = status.HTTP_409_CONFLICT
            return

        except redis.WatchError:
            response.status_code = status.HTTP_409_CONFLICT
            return


@app.get("/dataset/{dataset_id}", response_model=GetDatasetOut)
def get_dataset_info(dataset_id,
                     response: Response):
    r = redis.Redis()
    dataset_hash = Dataset.dataset_hash(dataset_id)
    res = r.hgetall(dataset_hash)
    if len(res) > 0:
        res = Dataset.from_db(**decode_none(res))

        response.status_code = status.HTTP_200_OK
        return GetDatasetOut(**res)

    response.status_code = status.HTTP_404_NOT_FOUND
    return None


@app.get("/dataset/{dataset_id}/data")
def get_dataset_data(dataset_id,
                     response: Response):
    r = redis.Redis()
    dataset_hash = Dataset.dataset_hash(dataset_id)
    result = r.hget(dataset_hash, "data")

    response.status_code = status.HTTP_200_OK
    return result


@app.get("/predict/{model_id}&{dataset_id}/")
def make_prediction(model_id,
                    dataset_id,
                    response: Response):
    r = redis.Redis()
    model_hash = Model.model_hash(model_id)
    dataset_hash = Dataset.dataset_hash(dataset_id)
    ...


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

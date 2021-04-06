## Data
Ames Housing Dataset: http://jse.amstat.org/v19n3/decock/AmesHousing.txt


## Prerequisites

To install project dependencies use:
```
pip install -r requirements.txt
```

To install mylib package use:
```
python setup.py install
```

To test mylib package use:
```
python -m pytest
```


## Commands

#### train.py

Script for training a model based on sklearn 'train' command.

| Argument | Required | Description                                      |
|:---------|:---------|--------------------------------------------------|
| -i       | true     | path to input file with data                     |


#### predict.py

Script for model evaluation. The test dataset should have the same format as the train dataset.

| Argument | Required | Description                                      |
|:---------|:---------|--------------------------------------------------|
| -i       | true     | path to input file with data                     |
| -m       | true     | path to .pkl serialized model                    |


## EDA & Cleansing

The entire process of analyzing and cleaning data is described in this notebook: [Cleansing&EDA.ipynb](https://gitlab.com/se_ml_course/2021/sotnikov.ad/-/blob/develop/notebooks/Cleansing&EDA.ipynb)


## Results

![alt text](notebooks/test_pairplot.png "Описание будет тут")

R<sup>2</sup> on test dataset: 0.918

MSE on test dataset (with box-cox transformation): 0.014


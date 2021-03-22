## Data
Ames Housing Dataset: http://jse.amstat.org/v19n3/decock/AmesHousing.txt


## Prerequisites
```
pip install -r requirements.txt
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

R^2 on test dataset: 0.918

MSE on test dataset (with box-cox transformation): 0.014


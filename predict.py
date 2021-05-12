import argparse
import pickle
import logging
import datetime
from uuid import uuid4

import numpy as np

from mylib import data_preprocessing

import warnings
warnings.filterwarnings('ignore')


def main():
    logging.debug(f'Start testing model at {datetime.datetime.now()}')
    logging.debug(f'Loading model from {args.model_path}')

    with open(args.model_path, 'rb') as file:
        model = pickle.load(file)

    logging.debug('Model loaded successful')

    _, _, X_test, y_test, _ = data_preprocessing(args.data_path)
    predictions = model.predict(X_test)

    logging.debug(f'Making predictions on test set...')
    logging.debug(f'R**2 on test set = {round(model.score(X_test, y_test), 3)}')
    logging.debug(f'MSE on test set = {round(sum((predictions - y_test) ** 2) / len(predictions), 3)}')

    np.savetxt(args.results_path + 'predictions.txt', predictions, newline=' ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test model.')

    parser.add_argument('--data_path', type=str, default='data/clean_data.csv',
                        help='path to the input file with data')
    parser.add_argument('--model_path', type=str, default='models/model.pkl',
                        help='path to trained model')
    parser.add_argument('--log_path', type=str, default='logs/predict/',
                        help='path to log folder')
    parser.add_argument('--results_path', type=str, default='results/',
                        help='path to folder with predicted values')
    args = parser.parse_args()

    log_file = args.log_path + 'predict_' + uuid4().hex + '.log'
    logging.basicConfig(level='DEBUG', filename=log_file)
    main()

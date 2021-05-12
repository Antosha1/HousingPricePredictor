from mylib import model
import argparse
import pickle
import logging
import datetime
from uuid import uuid4

from mylib import data_preprocessing

import warnings
warnings.filterwarnings('ignore')


def main():
    logging.debug(f'Model training starts at {datetime.datetime.now()}')

    X_train, y_train, _, _, _ = data_preprocessing(args.data_path)
    model_ = model.train(args.data_path)

    logging.debug(f'Training ends at {datetime.datetime.now()}')
    logging.debug(f'Making predictions on train set...')

    predictions = model_.predict(X_train)

    logging.debug(f'R**2 on train set = {round(model_.score(X_train, y_train), 3)}')
    logging.debug(f'MSE on train set = {round(sum((predictions - y_train) ** 2) / len(predictions), 3)}')

    pkl_filename = args.model_path + 'model.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model_, file)

    logging.debug(f'Model saved in {pkl_filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Model's train mode")
    parser.add_argument('--data_path', type=str, default='data/clean_data.csv',
                        help='path to the input file with data')
    parser.add_argument('--log_path', type=str, default='logs/train/',
                        help='path to the input file with data')
    parser.add_argument('--model_path', type=str, default='models/',
                        help='path to folder with trained models')
    args = parser.parse_args()

    log_file = args.log_path + 'train_' + uuid4().hex + '.log'
    logging.basicConfig(level='DEBUG', filename=log_file)
    main()

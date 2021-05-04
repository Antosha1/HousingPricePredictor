from mylib.model import predict
import argparse
import pickle
import numpy as np

from mylib import data_preprocessing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test model.')

    parser.add_argument('--data_path', type=str, nargs='+',
                        help='path to the input file with data')
    parser.add_argument('--model_path', type=str, nargs='+',
                        help='path to trained model')
    parser.add_argument('--log_path', type=str, nargs='+',
                        help='path to log folder')

    args = parser.parse_args()

    _, _, X_test, y_test, _ = data_preprocessing(args.data_path[0])

    print('Loading model...')
    with open(args.model_path[0], 'rb') as file:
        model = pickle.load(file)
    print('Model loaded successful')

    predictions = model.predict(X_test)
    print('R**2 on test = {:.3f}'.format(round(model.score(X_test, y_test), 3)))
    print('Test MSE = {:.3f}.'.format(round(sum((predictions - y_test) ** 2) / len(predictions), 3)))
    print("Min and max model's weights: {:.2f} и {:.2f}".format(round(min(model.coef_), 2),
                                                                round(max(model.coef_), 2)))

    np.savetxt('models/test.txt', predictions, newline=' ')

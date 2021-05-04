from mylib import model
import argparse
import pickle

from mylib import data_preprocessing


parser = argparse.ArgumentParser(description='Test model.')
parser.add_argument('--data_path', type=str, nargs='+',
                    help='path to the input file with data')
parser.add_argument('--log_path', type=str, nargs='+',
                    help='path to the input file with data')

args = parser.parse_args()

X_train, y_train, _, _, _ = data_preprocessing(args.data_path[0])

print('Model training...')
model_ = model.train(args.data_path[0])
print('Successful!')
print('R**2 on train = {:.3f}'.format(round(model_.score(X_train, y_train), 3)))
predictions = model_.predict(X_train)
print('Train MSE = {:.3f}.'.format(round(sum((predictions - y_train) ** 2) / len(predictions), 3)))

pkl_filename = 'models/model.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(model_, file)
print('Model saved in models/model.pkl')

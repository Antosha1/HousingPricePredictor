from mylib import model
import argparse
import pickle

parser = argparse.ArgumentParser(description='Test model.')
parser.add_argument('-i', type=str, nargs='+',
                    help='path to the input file with data')

args = parser.parse_args()

model = model.train(args.i[0])

pkl_filename = 'models/model.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

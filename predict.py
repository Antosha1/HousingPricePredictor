from mylib.model import test
import argparse
import pickle
import numpy as np

parser = argparse.ArgumentParser(description='Test model.')

parser.add_argument('-i', type=str, nargs='+',
                    help='path to the input file with data')
parser.add_argument('-m', type=str, nargs='+',
                    help='path to trained model')

args = parser.parse_args()

with open(args.m[0], 'rb') as file:
    model = pickle.load(file)

predictions = test(model, args.i[0])
print(predictions)

np.savetxt('models/test.txt', predictions, newline=' ')

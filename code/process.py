import mylib
import argparse
import pickle
import numpy as np

parser = argparse.ArgumentParser(description='Test model.')
parser.add_argument('-i', type=str, nargs='+',
                    help='path to the input file with data')
parser.add_argument('--train', action='store_true',
                    help='train mode')
parser.add_argument('-m', type=str, nargs='+',
                    help='path to the trained model')
parser.add_argument('--test', action='store_true',
                    help='test mode')
args = parser.parse_args()

if args.train:
    model = mylib.train(args.i[0])

    pkl_filename = "../models/model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)
elif args.test:
    with open(args.m[0], 'rb') as file:
        model = pickle.load(file)

    predictions = mylib.test(model, args.i[0])
    print(predictions)

    np.savetxt('../models/test.txt', predictions, newline=' ')

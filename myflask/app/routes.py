# -*- coding: utf-8 -*- 
from flask import render_template
from app import app
import subprocess

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Anton'}
    return render_template('index.html', title='Home Price Forecasting', user=user)

@app.route('/train')
def train():
    ps = subprocess.run(['python3', '../train.py', '-i', '../data/clean_data.csv'], capture_output=True)
    return ps.stdout

@app.route('/predict')
def predict():
    ps = subprocess.run(['python3', 'predict.py'], capture_output=True)
    return ps.stdout



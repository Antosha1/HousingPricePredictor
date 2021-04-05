# -*- coding: utf-8 -*- 
from flask import render_template
from app import app
import subprocess

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home Price Forecasting', user=user,
                           content='<img src="static/jaq.jpg" alt="">')

@app.route('/train', methods=['POST'])
def train():
    ps = subprocess.run(['python3', 'train.py'], capture_output=True)
    return ps.stdout

@app.route('/predict', methods=['POST'])
def predict():
    ps = subprocess.run(['python', 'predict.py'], capture_output=True)
    return ps.stdout



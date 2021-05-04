.PHONY: help requirements sync_data_from_drive clean test_environment train predict tests

PROJECT_NAME = mylib
PYTHON_INTERPRETER = python
BUCKET = 1d6pQPfjvGHEV9veXBB_Clq1_mYLvmyJb

include .env

requirements:
	$(PYTHON_INTERPRETER) setup.py install
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r test_requirements.txt
	$(PYTHON_INTERPRETER) -m pip install dvc
	$(PYTHON_INTERPRETER) -m pip install pydrive2

sync_data_from_drive:
	dvc remote add -d storage gdrive://$(BUCKET)

get_data:
	dvc pull

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

train:
	$(PYTHON_INTERPRETER) train.py \
        	--data_path ${PROCESSED_DATA} \
        	--log_path ${LOG_PATH}/train.log
	dvc add -R ${MODEL_PATH}
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push

predict:
	$(PYTHON_INTERPRETER) predict.py \
        	--data_path ${PROCESSED_DATA} \
        	--model_path ${MODEL_PATH}
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push

tests:
	pytest --cov=mylib --cov-branch --cov-report term-missing --cov-report xml:./results/coverage.xml tests --junitxml=./results/report.xml
	dvc add -R ${LOG_PATH}
	dvc commit
	dvc push

.DEFAULT: help
help:
	echo "make requirements: install python dependencies"
	echo "make test_environment: Test python environment is setup correctly"
	echo "make clean: Delete all compiled Python files"
	echo "make sync_data_from_drive: Download Data from Google-Drive using dvc"
	echo "make train: Train the model on previously created dataset and save logs to Google-Drive"
	echo "make predict: Predict using the trained model and save logs to Google-Drive"
	echo "make tests: run all tests, save reports"

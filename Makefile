.PHONY: build-dev destroy-dev deploy destroy

ENV := dev

PYTHON_VERSION := 3.7.4

build-dev:
	npm install
	# Check for version ${PYTHON_VERSION}, if it's not found, let's install
	pyenv versions | grep ${PYTHON_VERSION} || pyenv install ${PYTHON_VERSION}
	pyenv global ${PYTHON_VERSION}
	pipenv sync --dev --python $$(pyenv which python) || true

destroy-dev:
	pipenv --rm

deploy:
	serverless deploy

deploy-word-count:
	cd example/ &&\
	aws s3 cp wordcount.py "s3://datenworks-wordcount-example/pyspark/" &&\
	aws s3 cp lorem.txt "s3://datenworks-wordcount-example/dataset/" &&\
	cd ../

destroy:
	serverless remove

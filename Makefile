.PHONY: build-dev destroy-dev deploy destroy

ENV := dev

PYTHON_VERSION := 3.7.4

EMR_SLAVE_SG := 'security-group-for-slaves'
EMR_MASTER_SG := 'security-group-for-master'
EMR_SERVICE_ACCESS_SG := 'emr-service-security-group'
SECURITY_CONFIGURATION := 'emr-data-encryption'
AUTOSCALING_ROLE := 'AmazonElasticMapReduceforAutoScalingRole'
JOB_FLOW_ROLE := 'EMR_EC2_DefaultRole'
SERVICE_ROLE := 'EMR_DefaultRole'

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
	aws s3 cp wordcount.py "s3://${EXAMPLE_BUCKET}/pyspark/" &&\
	aws s3 cp lorem.txt "s3://${EXAMPLE_BUCKET}/dataset/" &&\
	cd ../

destroy:
	serverless remove

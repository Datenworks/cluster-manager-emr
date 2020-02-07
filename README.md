# The EMR Cluster Manager

## Overview

AWS Lambda function being managed through Serverless Framework responsible for:

 - receiving input from AWS Step Functions (State Machine)
 - treating data and parsing values to configure the AWS EMR
 - passing the output to AWS EMR execution
 - monitoring the AWS EMR task execution

## Getting Started

### Requirements

In order to execute deployment for this project, some tools and frameworks are necessary:

 - python 3+ installed
 - pyenv
 - pipenv
 - [Serverless framework](https://serverless.com/)
 - make (CMake, GNU Make or BSD Make)
 - [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
 - Terraform

You can procede to deployment if you already have these tools

### Deploy

There a Terraform module provisioning the resources into aws account.
Apply the module to create the necessaries resources into your AWS Account

- Create the State Machine responsible for Cluster Manager
- Create e SNS Topic to receive messages when the Cluster Manager fails
- Create the roles for EMR Cluster
- Can be added more custom roles by your desire and necessities

```
cd terraform/base
terraform init
```
```
terraform plan
terraform apply
```

A compressed zip for the project requirements is necessary in order to be uploaded to AWS S3 bucket.
This zip file must be behind the limits for AWS Lambda, one of them are size (<250MB)

To manage this zip file, a plugin in the serverless framework must be included with

```bash
serverless plugin install --name serverless-python-requirements
```

After, you'll find a [makefile](Makefile) in the repository root to help with the next steps

The deployment can be parameterized to facilitate the hand-work:

e.g.:

```bash
make ENV=dev \
EMR_SLAVE_SG='security-group-for-slaves' \
EMR_MASTER_SG='security-group-for-master' \
EMR_SERVICE_ACCESS_SG='emr-service-security-group' \
deploy
```

### Cleanup

To destroy everything, there's also a command, which is pretty simpler

```bash
make destroy
```

This will delete the Serverless CloudFormation stack for this application and the Spark job in the AWS S3 bucket

### Requirements

* Python 3
* Node JS (for the Serverless CLI)
* Serverless Framework
* Terraform


### The payload
Can be used by another State Machine, lambda or executed directly

Payload received by the State Machine:
```

{
    "data":{
        "name": "your-cluster-name",
        "resource": "your-resource-name",
        "arguments": [
            {
                "Key": "--conf",
                "Value": "yournamespace.blablabla.yourargument=yourvalue"
            }
        ],
        "pyfiles": "s3a://path_to_python_files.zip",
        "subnet": "subnet-id",
        "master_type": "m5.xlarge",
        "core_type": "m5.2xlarge",
        "count": "6",
        "release": "emr-5.27.0",
        "region": "us-east-1",
        "log_bucket": "s3://log_bucket",
        "entrypoint": "s3a://path_to_pyspark_file.py",
        "mem_driver": "8G",
        "mem_executor": "16G",
        "spark_packages": ["sparkpackage1", "sparkpackage2"],
        "jar_files": ["path_to_jarfile1.jar", "path_to_jarfile2.jar"],
        "multiple_steps": "ENABLED / DISABLED",
        "bootstrap_steps": [
            {
                "arguments": ["sudo", "pip", "install", "something"]
            }
        ]
    }
}
```
Also can be passed as base64 string.
```
{
    "data": "eyJqb2JfbmFtZSI6ICJ0aGUtbmFtZS1vZi10aGUtam9iIiwgInJlc291cmNlIjogInJlc291cmNlIGJlaWduIGV4ZWN1dGVkIiwgIm5hbWVzcGFjZSI6ICJ0aGUtbmFtZXNwYWNlLXRvLW1vdW50LXRoZS1hcmd1bWVudDogbmFtZXNwYWNlLmFyZ25hbWU9dmFsdWUiLCAiYXJndW1lbnRzIjogW3siYXJndW1lbnQiOiAiYXJndW1lbnQtbmFtZSIsICJ2YWx1ZSI6ICJ0aGUtdmFsdWUtb2YtYXJnIn1dLCAiY29kZV9maWxlcyI6ICJ0aGUtcGF0aC10by1jb2RlLWZpbGVzLXppcCBpbiBzMyIsICJjb2RlX2VudHJ5cG9pbnQiOiAid"
}
```
## Example Word Count

Deploy the word-count example
```
make EXAMPLE_BUCKET="name-of-example-bucket" \
    deploy-word-count
```

Payload to execute the example of wordcount:
```
{
    "data":{
        "name": "wordcount",
        "resource": "resource-name",
        "namespace": "wordcount",
        "arguments": [
            {
                "argument": "input_bucket",
                "value": "your-bucket-example"
            },
            {
                "argument": "output_bucket",
                "value": "your-bucket-example"
            },
            {
                "argument": "key_path",
                "value": "dataset/lorem.txt"
            }
        ],
        "code_files": "s3://your-bucket-example/pyspark/wordcount.py",
        "entrypoint": "s3://your-bucket-example/pyspark/wordcount.py",
        "mem_executor": "8G",
        "mem_driver": "4G",
        "master_type": "m5.xlarge",
        "count": "3",
        "slave_type": "m5.2xlarge",
        "release": "emr-5.28.0",
        "region": "us-east-1",
        "log_bucket": "your-log-bukcket-uri",
        "subnet": "your-subnet",
        "spark_packages": [],
        "jar_files": [],
        "multiple_steps": "ENABLED",
        "bootstrap_steps": []
    }
}
```

[![DatenWorks](https://www.datenworks.com/img/logo.png)](https://www.datenworks.com/)

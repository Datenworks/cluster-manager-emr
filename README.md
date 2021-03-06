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
    deploy
```

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
        "name": "the-name-of-the-job",
        "resource": "resource beign executed",
        "namespace": "the-namespace-to-mount-the-argument: namespace.argname=value",
        "arguments": [
            {
                "argument": "argument-name",
                "value": "the-value-of-arg"
            }
        ],
        "code_files": "the-path-to-code-files-zip in s3",
        "entrypoint": "the-code-file-that-will-be-executed",
        "mem_executor": "optional, default is 16G",
        "mem_driver": "optional, default is 8G",
        "master_type": "optional, default is m5.xlarge",
        "slave_type": "optional(core), default is m5.2xlarge",
        "count": "3",
        "release": "emr_release",
        "region": "emr_region",
        "log_bucket": "uri for the log bucket",
        "subnet": "subnet_id for execute the emr",
        "spark_packages": ["package1", "package2", "keep empty if dont have"]
    }
}
```
Also can be passed as base64 string.
```
{
    "data": "eyJqb2JfbmFtZSI6ICJ0aGUtbmFtZS1vZi10aGUtam9iIiwgInJlc291cmNlIjogInJlc291cmNlIGJlaWduIGV4ZWN1dGVkIiwgIm5hbWVzcGFjZSI6ICJ0aGUtbmFtZXNwYWNlLXRvLW1vdW50LXRoZS1hcmd1bWVudDogbmFtZXNwYWNlLmFyZ25hbWU9dmFsdWUiLCAiYXJndW1lbnRzIjogW3siYXJndW1lbnQiOiAiYXJndW1lbnQtbmFtZSIsICJ2YWx1ZSI6ICJ0aGUtdmFsdWUtb2YtYXJnIn1dLCAiY29kZV9maWxlcyI6ICJ0aGUtcGF0aC10by1jb2RlLWZpbGVzLXppcCBpbiBzMyIsICJjb2RlX2VudHJ5cG9pbnQiOiAidGhlLWNvZGUtZmlsZS10aGF0LXdpbGwtYmUtZXhlY3V0ZWQiLCAibWVtX2V4ZWN1dG9yIjogIm9wdGlvbmFsLCBkZWZhdWx0IGlzIDE2RyIsICJtZW1fZHJpdmVyIjogIm9wdGlvbmFsLCBkZWZhdWx0IGlzIDhHIiwgIm1hc3Rlcl90eXBlIjogIm9wdGlvbmFsLCBkZWZhdWx0IGlzIG01LnhsYXJnZSIsICJzbGF2ZV90eXBlIjogIm9wdGlvbmFsKGNvcmUpLCBkZWZhdWx0IGlzIG01LjJ4bGFyZ2UiLCAicmVsZWFzZSI6ICJlbXJfcmVsZWFzZSIsICJyZWdpb24iOiAiZW1yX3JlZ2lvbiIsICJsb2dfYnVja2V0IjogInVyaSBmb3IgdGhlIGxvZyBidWNrZXQiLCAic3VibmV0IjogInN1Ym5ldF9pZCBmb3IgZXhlY3V0ZSB0aGUgZW1yIiwgInNwYXJrX3BhY2thZ2VzIjogWyJwYWNrYWdlMSIsICJwYWNrYWdlMiIsICJrZWVwIGVtcHR5IGlmIGRvbnQgaGF2ZSJdfQ=="
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
        "spark_packages": [""]
    }
}
```

[![DatenWorks](https://www.datenworks.com/img/logo.png)](https://www.datenworks.com/)

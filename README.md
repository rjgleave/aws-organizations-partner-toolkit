Partner Toolkit for AWS Organizations 
==================================================

This repository contains code to automate the setup of the master payer account and provide separation of concerns between the partner role (billing) and the institution role (org management).

The scripts included in this toolkit will implement the following architecture below, including user groups, profiles, IAM policies, Service Control Policies (SCPs), Organization Units (OUs), etc. 

![Reference Architecture](https://github.com/rjgleave/aws-batch-api-submitter/blob/master/assets/trigger-batch-using-api-gateway.png)

![](https://github.com/rjgleave/aws-batch-api-submitter/blob/master/assets/Trigger-AWS-Batch-Integration-Job-Using-API-Gateway.png)

In this example, an on-premise process runs, followed by a cloud-based process.  At the completion of the on-premise process, an http message is posted to an api, which saves the transaction in DynamoDB.  A trigger on the dynamoDB table invokes a state machine (AWS Step Functions) which submits the job corresponding to the message.  Step Functions will monitor the job for success or failure, until its completion.   


What's Here
-----------

This repo includes:

1. README.md - this file
2. FOLDER: dynamo - this contains code to help build the sample 
transaction table in dynamoDB.  It includes:
    *   schema.json - an example of the dynamoDB schema data structure
    *   read_dynamo_stream.py - the lambda program which reads the dynamodb streams
    *   test_streams.json - a sample stream file for testing the lambda above.
3. FOLDER: api-gateway - contains templates to help build and test the API REST interface
    *   api_gateway_mapping_template.json - this is the mapping document used to create the proxy api for the state machine service.
    *   test_message.json - copy the json document and use to test the API.
4. FOLDER: state_machine  - components to build the state machine
    *   JobStatusPoller.py - a lambda to poll the status of batch jobs.
    *    SubmitJobFunction.py - lambda function to submit a batch job. 
    *   JobStatusPollerStateMachine.json - definition of the state machine
    *   input-template.json - the document used to submit the state machine

Setup Instructions
------------------

Working Backwards, do the following:

1. Create the state machine.  The easiest way to do this is to use the online jumpstart which will build it for you.  See instructions here:
![Reference Architecture](https://github.com/rjgleave/aws-batch-api-submitter/blob/master/assets/step-function-sample-projects.png)

2. Use the schema to build DynamoDB table.   Make sure you turn on streaming.
3. Install the lambda to read the dynamodb stream.   You will need to modify it to pass in the input document and ARN of the state machine.    You can test it using the test_streams.json document.
4. Create the API.  Use the provided mapping document.



__Additional Resources__

Blog: Using Amazon API Gateway as a proxy for DynamoDB
https://aws.amazon.com/blogs/compute/using-amazon-api-gateway-as-a-proxy-for-dynamodb/

SWS Step Functions
https://aws.amazon.com/step-functions/
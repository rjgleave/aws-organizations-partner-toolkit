#Copyright 2008-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

#Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#http://aws.amazon.com/apache2.0/
#or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


#!/usr/bin/env python

from __future__ import print_function
import boto3
import botocore
import time
import sys
import argparse

'''AWS Organizations Create Account and Provision Resources via CloudFormation

This module creates a new account using Organizations, then calls CloudFormation to deploy baseline resources within that account via a local tempalte file.

'''

__version__ = '0.1'
__author__ = '@author@'
__email__ = '@email@'


def create_organization(
        feature_set):

    '''
        Create a new AWS organization for the account. 
    '''

    client = boto3.client('organizations')
    try:
        create_organization_response = client.create_organization(FeatureSet=feature_set)

    except botocore.exceptions.ClientError as e:
        print(e)
        sys.exit(1)

    print('Creating a New Organization...')
    print(create_organization_response)
    print('')

    return create_organization_response


def describe_account(
        account_id):

    '''
        Describe the AWS account 
    '''

    client = boto3.client('organizations')
    try:
        describe_account_response = client.describe_account(AccountId=account_id)

    except botocore.exceptions.ClientError as e:
        print(e)
        sys.exit(1)

    print('describe account here')
    print(describe_account_response)

    return describe_account_response


def list_roots():

    '''
        List the roots in the current organization 
    '''

    client = boto3.client('organizations')
    try:
        list_roots_response = client.list_roots()

    except botocore.exceptions.ClientError as e:
        print(e)
        sys.exit(1)

    print('List of Roots here:')
    print(list_roots_response)

    return list_roots_response


def deploy_resources(credentials, template, stack_name, stack_region, admin_username, admin_password):

    '''
        Create a CloudFormation stack of resources within the new account
    '''

    datestamp = time.strftime("%d/%m/%Y")
    client = boto3.client('cloudformation',
                          aws_access_key_id=credentials['AccessKeyId'],
                          aws_secret_access_key=credentials['SecretAccessKey'],
                          aws_session_token=credentials['SessionToken'],
                          region_name=stack_region)
    print("Creating stack " + stack_name + " in " + stack_region)

    creating_stack = True
    while creating_stack is True:
        try:
            creating_stack = False
            create_stack_response = client.create_stack(
                StackName=stack_name,
                TemplateBody=template,
                Parameters=[
                    {
                        'ParameterKey' : 'AdminUsername',
                        'ParameterValue' : admin_username
                    },
                    {
                        'ParameterKey' : 'AdminPassword',
                        'ParameterValue' : admin_password
                    }
                ],
                NotificationARNs=[],
                Capabilities=[
                    'CAPABILITY_NAMED_IAM',
                ],
                OnFailure='ROLLBACK',
                Tags=[
                    {
                        'Key': 'ManagedResource',
                        'Value': 'True'
                    },
                    {
                        'Key': 'DeployDate',
                        'Value': datestamp
                    }
                ]
            )
        except botocore.exceptions.ClientError as e:
            creating_stack = True
            print(e)
            print("Retrying...")
            time.sleep(10)

    stack_building = True
    print("Stack creation in process...")
    print(create_stack_response)
    while stack_building is True:
        event_list = client.describe_stack_events(StackName=stack_name).get("StackEvents")
        stack_event = event_list[0]

        if (stack_event.get('ResourceType') == 'AWS::CloudFormation::Stack' and
           stack_event.get('ResourceStatus') == 'CREATE_COMPLETE'):
            stack_building = False
            print("Stack construction complete.")
        elif (stack_event.get('ResourceType') == 'AWS::CloudFormation::Stack' and
              stack_event.get('ResourceStatus') == 'ROLLBACK_COMPLETE'):
            stack_building = False
            print("Stack construction failed.")
            sys.exit(1)
        else:
            print(stack_event)
            print("Stack building . . .")
            time.sleep(10)

    stack = client.describe_stacks(StackName=stack_name)
    return stack
  

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--account_name', required=True)
    parser.add_argument('--account_email', required=True)
    parser.add_argument('--account_role',
                        default='OrganizationAccountAccessRole')
    parser.add_argument('--template_file',
                        default='baseline.yml')
    parser.add_argument('--stack_name',
                        default='Baseline')
    parser.add_argument('--stack_region',
                        default='us-east-1')
    parser.add_argument('--admin_username', required=True)
    parser.add_argument('--admin_password', required=True)
    #parser.add_argument('--account_id', default='166631568452', required=True)

    args = parser.parse_args(arguments)
    
    access_to_billing = "DENY"
    organization_unit_id = None
    scp = None


    '''
    # describe the account                
    account_id = '166631568452'
    print("Displaying account: " + account_id)
    describe_account_response = describe_account(account_id)
    '''

    # 1 - build users, groups, policies via cloudformation
    print("Deploying resources from " + args.template_file + " as " + args.stack_name + " in " + args.stack_region)
    template = get_template(args.template_file)
    stack = deploy_resources(credentials, template, args.stack_name, args.stack_region, args.admin_username, args.admin_password)
    print(stack)
    print("Resources deployed for account " + account_id + " (" + args.account_email + ")")
     
    # 2 - create an organization
    feature_set = 'ALL'
    print("Creating organization...  FeatureSet = " + feature_set)
    create_organization_response = create_organization(feature_set)
    
    # 3 - list root of the org
    list_roots_response = list_roots()

    # 4 - create service control policies

    # 5 - attach SCPs to the OUs
    # root - FullAWSAccessSCP
    # parent OU - DenyAllBillingSCP 


    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

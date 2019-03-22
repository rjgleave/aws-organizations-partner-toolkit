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



def get_template(template_file):

    '''
        Read a template file and return the contents
    '''

    print("Reading resources from " + template_file)
    f = open(template_file, "r")
    cf_template = f.read()
    return cf_template


def deploy_resources(template, stack_name, stack_region, org_admin_password, partner_admin_password):

    '''
        Create a CloudFormation stack of resources within the new account
    '''

    datestamp = time.strftime("%d/%m/%Y")
    client = boto3.client('cloudformation',
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
                        'ParameterKey' : 'OrgAdminPassword',
                        'ParameterValue' : org_admin_password
                    },
                    {
                        'ParameterKey' : 'PartnerAdminPassword',
                        'ParameterValue' : partner_admin_password
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

    parser.add_argument('--org_admin_password', required=True)
    parser.add_argument('--partner_admin_password', required=True)

    parser.add_argument('--template_file',
                        default='create-all-resources.yaml')
    parser.add_argument('--stack_name',
                        default='master-payer-resources')
    parser.add_argument('--stack_region',
                        default='us-east-1')

    args = parser.parse_args(arguments)

    access_to_billing = "DENY"
    organization_unit_id = None
    scp = None

    print("Deploying resources from " + args.template_file + " as " + args.stack_name + " in " + args.stack_region)
    template = get_template(args.template_file)
    stack = deploy_resources(template, args.stack_name, args.stack_region, args.org_admin_password, args.partner_admin_password)
    print(stack)
    print("Resources deployed for account " + account_id + " (" + args.account_email + ")")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

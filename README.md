Partner Toolkit for AWS Organizations 
==================================================

This repository contains code to automate the setup of the master payer account and provide separation of concerns between the partner role (billing) and the institution role (org management).

The scripts included in this toolkit will implement the reference architecture shown below, including user groups, profiles, IAM policies, Service Control Policies (SCPs), Organization Units (OUs), etc. 

![Reference Architecture](https://github.com/rjgleave/aws-organizations-partner-toolkit/blob/master/assets/AWS-Orgs-for-Resellers.png)

This model allows the partner to maintain ultimate ownership of the master payer account, including the root account itself.  The root account will create the organization, a parent OU and service control policies to apply to the organization root.   In addition, a billing administrator will be granted full rights to all billing and cost functions.  

The institution will be given rights to all AWS services at any OU below the Organization root.   This includes full rights over the creation of OUs, SCPs and the ability to apply SCPs at any OU below the org root.  The institution admin can also invite accounts to join the organization.  No institution account or user will have the ability to access billing or cost features.   This includes any member accounts invited into the organization.


What's Here
-----------

This repo includes:

1. README.md - this file
2. FOLDER: python - 
    *   the root organization - with all AWS services enabled
    *   the institution's parent OU
    *   service control policies (SCPs)
3. FOLDER: cloudformation - this contains cloudformation code to create
the following objects in the master billing account, including:
    *   IAM admin groups, users and policies
    *   IAM admin user profiles 
    *   IAM policies to protect the root organization and prevent unauthorized access to billing.
4. FOLDER: scp-examples  
5. FOLDER: iam-policy-examples

Setup Instructions
------------------

Working Backwards, do the following:

1. Create a master payer account.

2. Run the python script to create the organization, parent OU and SCPs.  This will also apply the SCPs

3. Run ghe cloudformation template to build all IAM groups, user profiles and policies.
4. Invite accounts into the new organization.



__Additional Resources__

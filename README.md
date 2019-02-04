Partner Toolkit for AWS Organizations 
==================================================

This repository contains code to automate the setup of the master payer account and provide separation of concerns between the partner role (billing) and the institution role (org management).

The scripts included in this toolkit will implement the reference architecture shown below, including user groups, profiles, IAM policies, Service Control Policies (SCPs), Organization Units (OUs), etc. 

![Reference Architecture](https://github.com/rjgleave/aws-organizations-partner-toolkit/blob/master/assets/AWS-Orgs-for-Resellers.png)

This model allows the partner to maintain ultimate ownership of the master payer account, including the root account profile.  The root account profile will be used to create an organization, a parent OU and service control policies to apply to the organization root.  It will also create all IAM objects (groups, users and policies) to support billing and organization activities in the master payer account.  

Day-to-day activities in the master payer account will be carried out by the billing administrator and org administrator profiles.   The billing administrator will be granted full rights to all billing and cost functions.  The org administrator will be granted rights to all AWS services at any OU below the Organization root.  This includes the ability to define OUs, SCPs and the ability to apply SCPs at any OU below the org root.  The org admin can also invite accounts to join the organization.  

Service control policies applied at the organization root will automatically deny access to billing and cost features for any member account that joins the organization.   However, SCPs will also automatically grant full access to all other AWS services to those same member accounts.


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

Working Backwards, execute the following steps:

1. Create a master payer account.

2. Create the organization.   Instructions here: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_create.html  NOTE: Specify that you want to create the organization with ALL FEATURES enabled.

3. Create an OU within the root in your organization.   Instructions here: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html Add other OUs to your organizational hierarchy as desired.

4. Create Service Control Policies.    See the SCP folder described above for examples.  You should tailor the SCPs to meet your own security requirements and needs.  Typically, resellers may want to allow the use of all AWS services but deny all billing access and prevent changing SCPs applied at the root OU.  Please NOTE: some of the example policies are defined to affect specific resource ARNs (scan for Resources with the account number 111111111111.  Substitute your root OU ARN and account#)

3. Run the cloudformation template to build all IAM groups, user profiles and policies.

4. Invite accounts into the new organization.



__Additional Resources__

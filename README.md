Partner Toolkit for AWS Organizations 
==================================================

This repository contains code to automate the setup of the master payer account and provide separation of concerns between the partner role (billing) and the institution role (org management).

The scripts included in this toolkit will implement the reference architecture shown below, including user groups, profiles, IAM policies, Service Control Policies (SCPs), Organization Units (OUs), etc. 

![Reference Architecture](https://github.com/rjgleave/aws-organizations-partner-toolkit/blob/master/assets/AWS%20Orgs%20for%20Resellers.png)

This model allows the partner to maintain ultimate ownership of the master payer account, including the root account profile.  The root account profile will be used to create an organization, a parent OU and service control policies to apply to the organization root.  It will also create all IAM objects (groups, users and policies) to support billing and organization activities in the master payer account.  

Day-to-day activities in the master payer account will be carried out by the billing administrator and org administrator profiles.   The billing administrator will be granted full rights to all billing and cost functions.  The org administrator will be granted rights to all AWS services at any OU below the Organization root.  This includes the ability to define OUs, SCPs and the ability to apply SCPs at any OU below the org root.  The org admin can also invite accounts to join the organization.  

Service control policies applied at the organization root will automatically deny access to billing and cost features for any member account that joins the organization.   However, SCPs will also automatically grant full access to all other AWS services to those same member accounts.


What's Here
-----------

This repo includes:

1. README.md - this file
2. FOLDER: python (FUTURE - to replace manual Org creation steps below)
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

Working backwards, execute the following steps:

1. Create a master payer account.

2. Create your organization.   Instructions here: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_create.html  NOTE: Specify that you want to create the organization with ALL FEATURES enabled.

3. Create an OU within the root in your organization.   Instructions here: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html Add other OUs to your organizational hierarchy as desired.

4. Create any service control policies that you would like to see enforced across all member accounts in the organization.  Then attach them to the root OU.  Any SCPs applied at the root OU will cascade down to all member accounts in the organization.  See the SCP folder described above for examples.  You should tailor the SCPs to meet your own business requirements and operating model.  

Typically, resellers will want to whitelist the use of all AWS services for their customer accounts (see FullAWSAccessSCP).   

Also, resellers may decide to deny all billing access to member accounts (see DenyAllBillingSCP for example).  More examples identified here: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-permissions-ref.html#ExampleAllowAllDenyBilling

 Resellers will want to protect the SCPs that they define.  One way to do this is to specifically DENY changes to those specific policies.  Some of the example policies in this repo are defined to protect specific resource ARNs  In these examples you can scan for Resources with the account number 101010101010.  You will need to substitute your root OU ARN and account numbers if you want to use these examples.   
 
 Another strategy to protect SCPs is to prevent deny access to the root OU for any customer admins (see DenyAttachPolicyRootOU).  Since all reseller SCPs will be attached at the root OU, this will protect them.   

3. Run the cloudformation template to build all IAM groups, user profiles and policies.

4. Invite accounts into the new organization.


__Additional Resources__

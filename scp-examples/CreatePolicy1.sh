aws organizations create-policy --content file://DenyAttachPolicyrootOU.json --name AllowAllS3Actions, --type SERVICE_CONTROL_POLICY --description "Deny Attaching SCPs to the root OU"


aws organizations create-policy --content file://DenyAttachPolicyrootOU.json --name DenyAttachPolicyRootOU, --type SERVICE_CONTROL_POLICY --description "test"
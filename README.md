# Automatically update Route 53 DNS

REQUIREMENTS: *
- python3
- awscli
- epel-release repository

A script to update an EC2 instances ipv4 address in Route53 (update the 'A' record) with the current public ipv4 address assigned by AWS

This script relies on the fact that AWS allows you to access meta-data from a running EC2 instance. Included in the metat-data is the currently assinged public ipv4 address. 
Also since AWS allows "User Data" to be passed in and executed as root upon an EC2 instances boot, you can add this script as part of your "User Data".
If you want this to work for any "new" EC2 vms that you create then you need to create a base AMI that has this script alread installed in a location of your choosing.


You need to supply a "hosted-zone-id" and a FQDN (fully qualified domain name)
  - The "hosted-zone-id" is provided by AWS on your Hosted Zones page
  - The FQDN is whatever you have setup in Route 53

Since the instance you are running this script on needs to make changes to Route53, you need to create a [Role based Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) allowing such
access and assign the role to the instance you are running this script on. You can assign this role at the same time you are creating the instance.

Your script that you will place in your [User data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) section will look like this:
  
#cloud-boothook
#!/usr/bin/bash

yum install –y update
yum install –y epel-release
yum install –y python36
yum install –y awscli

cd /root/route53
/root/route53/update.py A3KJXFJZGKJY0P your.domain.com
  
Also keep in mind that rebooting the intance will not get you a new public ipv4 addres from AWS. You must start the instance from a "shutdown" state in order for the "User Data" to take effect.

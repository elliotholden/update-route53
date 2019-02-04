# Automatically update Route 53 DNS

REQUIREMENTS:
- python3
- awscli
- epel-release repository

A script to update an EC2 instances ipv4 address in Route53 (update the 'A' record) with the current public ipv4 address assigned by AWS.


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


1. You need to give the instace you are running this script on permisison to update your Route53 hosted zones. You can do this after you have created the instance. Or duing the instance creation procces.
2. First create a “resource record” in the “hosted zone” of your choice in Route53. This script only works with “A” records for now so create an “A” record with a domain name. Set the value (IP address) of the A record to something that will go nowhere like 0.0.0.0 (this will get updated when the script runs)
2. You will need Python 3, AWS CLI installed.
	If you are using CentOS do the following:
	* sudo yum install –y update
	* sudo yum install –y epel-release
	* sudo yum install –y python36
	- sudo yum install –y awscli

	If you are using Amaon Linux 2 do the following:
   -  sudo yum update
	*  sudo yum install python3

3. Put the "update.py" and "template.json" files in a directory together (maybe /root/route53) 

4. Make sure "update.py" is executable then run the command.
    - the first argument to the command is the “hosted zone ID” and the second should be the domain name you are updating.

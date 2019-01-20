# update-route53.py
# update-route53-cli.py

A script to update an EC2 instances ipv4 address in Route53 (update the 'A' record) with the current public ipv4 address assigned by AWS

This script relies on the fact that AWS allows you to access meta-data from a running EC2 instance. Included in the metat-data is the currently assinged public ipv4 address. Also since AWS allows "User Data" to be pass in and executed as root upon an EC2 instances boot, you can add this script as part of your "User Data".

You need to supply a "hosted-zone-id" and an "absolute file path"
  - The "hosted-zone-id" is provided by AWS on your Hosted Zones page
  - The "absolute file path" is the path from where you are running this script on your system (output files will be written there)
If you are running the cli version of this program you will be prompted for both as you run the program from the command line.
If you are running the non-cli version then you must supply the "hosted-zone-id" and an "absolute file path" inside the script.

Since the instance you are running this script on needs to make changes to Route53, you need to create Role based Policy allowing such
access and asign the role to the instance you are running this script on.

The non-cli version is desinged to be run as "User Data" as your instance boots up. So you would have something similar to the following
inside your "User Data" area:
  
  #cloud-boothook
  #!/usr/bin/bash

  /path/to/script/update-dns.py
  
Also keep in mind that rebooting the intance will not get you a new public ipv4 addres from AWS. You must start the instance from a "shutdown" state in order for the "User Data" to take effect.

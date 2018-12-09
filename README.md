# update-route53.py
# update-route53-cli.py

A script to update an EC2 instances ipv4 address in Route53 (update the 'A' record) with the current public ipv4 address assigned by AWS

You need to supply a "hosted-zone-id" and an "absolute file path"
  - The "hosted-zone-id" is provided by AWS on your Hosted Zones page
  - The "absolute file path" is the path to where you are running this script on your system (output files will be written there)
If you are running the cli version of this program you will be prompted for both as you run the program from the command line.
If you are running the non-cli version then you must supply the "hosted-zone-id" and an "absolute file path" inside the script.

Since the instance you are running this script on needs to make changes to Route53, you need to create Role based Policy allowing such
access and asign the role to this instance.

The non-cli version is desinged to be run as "User Data" as your instance boots up. So you would have something similar to the following
inside your "User Data" area:
  
  #cloud-boothook
  #!/usr/bin/bash

  /path/to/script/update-dns.py

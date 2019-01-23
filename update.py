#!/usr/bin/python3

import os
import re
import sys

my_hosted_zone_id = sys.argv[1] 
my_domain_name = sys.argv[2] 

# This next step is not really required except for the fact that I want to know what the "A" records in my hoted zone look like before I make any changes
os.system('aws route53 list-resource-record-sets --hosted-zone-id ' + my_hosted_zone_id + ' --query "ResourceRecordSets[?Type == \'A\']" &>' + "./" + 'previous-record-set.json')

# Getting the public IPv4 address assinged to this instance from the AWS provided meta-data
public_ipv4_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()

# Open template file and replace the IP address and the domain name 
with open("./" + 'template.json') as myfile:
	my_json = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', public_ipv4_address, myfile.read())
	my_json = re.sub('my\.domain\.name', my_domain_name, my_json)

# Write the new record set to a file
f = open("./" + 'record-set.json', 'w')
f.write(my_json)
f.close()

# Run the AWS cli commad to update Route53 with the new IP address. Also save any errors or output to a file so you know what was done.
os.system('aws route53 change-resource-record-sets --hosted-zone-id ' + my_hosted_zone_id + ' --change-batch file://' + "./" + 'record-set.json &>' + "./" + 'change-record-set.out')


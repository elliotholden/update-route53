#!/usr/bin/python3

import os
import re

my_hosted_zone_id = '123456789abcde' # Change this to "your" hosted-zone-id. Use "aws route53 list-hosted-zones" to get your hosted-zone-id
my_domain_name = 'my.domain.name' # Change this to the domain name that you want want to up the the public ipv4 address for.
my_file_path = '/path/to/script/' # Change this to the path where "this" script is located (output files get written here as well)

os.system('aws route53 list-resource-record-sets --hosted-zone-id ' \
				+ my_hosted_zone_id + \
				' --query "ResourceRecordSets[?Type == \'A\']" \
				>' + my_file_path + 'previous-record-set.json 2>' + my_file_path + 'get-previous-record-set-errors.txt')

public_ipv4_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()

with open(my_file_path + 'record-set-template.json') as myfile:
	my_json = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', public_ipv4_address, myfile.read())
	my_json = re.sub('my\.domain\.name', my_domain_name, my_json)

f = open(my_file_path + 'new-record-set.json', 'w')
f.write(my_json)
f.close()

os.system('aws route53 change-resource-record-sets --hosted-zone-id ' \
				+ my_hosted_zone_id + \
				' --change-batch file://' + my_file_path + 'new-record-set.json \
				&>' + my_file_path + 'change-record-set-output.txt')

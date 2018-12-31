#!/usr/bin/python3

import os
import re

my_hosted_zone_id = 'Z2L2TMCJU3N9X3'
my_domain_name = 'lfcs.scriptbabies.com'
my_file_path = '/home/elliot/update-dns/'

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

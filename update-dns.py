#!/usr/bin/python3

##### This script gets the current public ipv4 address for this instance as it boots up, creates a new-record-set.json file the updates Route 53 DNS #####

import os
import re

# Pull down the current Route53 'A' record for lfcs.scriptbabies.com
os.system('aws route53 list-resource-record-sets --hosted-zone-id Z2L2TMCJU3N9X3 --query "ResourceRecordSets[?Type == \'A\']" >./get-previous-record-set-output.txt 2>./get-previous-record-set-errors.txt')


# Get the current Public IPV4 address assigned to this instance
current_ip_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()
		# https://stackoverflow.com/questions/1410976/equivalent-of-bash-backticks-in-python

#The 'with' statement usually encapsulates some setup/teardown open/close actions. So basically the file is explicitly closed when you're done with it.
with open('record-set-template.json') as myfile:
	my_json = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', current_ip_address, myfile.read())

f = open('updated-record-set.json', 'w')
f.write(my_json)
f.close()

os.system('aws route53 change-resource-record-sets --hosted-zone-id Z2L2TMCJU3N9X3 --change-batch file://new-record-set.json &>dns-record-change.output')


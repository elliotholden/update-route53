#!/usr/bin/python3

##### This script gets the current public ipv4 address for this instance as it boots up, creates a new-record-set.json file the updates Route 53 DNS #####

import os	# This is so you can make system calls
import re	# This is so you can use regular expressions

my_hosted_zone_id = '123456789abcde' # You hosted-zone-id
my_domain_name = 'my.domain.name' # The domain name that you are changing the 'A' record on
my_file_path = '/path/to/script/' # Path to the where this script is located (output files will be written there as well)

# Pull down the current Route53 'A' record for your hosted zone, so you know what it was before you do the update
os.system('aws route53 list-resource-record-sets --hosted-zone-id ' \
				+ my_hosted_zone_id + \
				' --query "ResourceRecordSets[?Type == \'A\']" \
				>' + my_file_path + 'previous-record-set.json 2>' + my_file_path + 'get-previous-record-set-errors.txt')

# Get the current Public IPV4 address assigned to this instance
public_ipv4_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()
		# https://stackoverflow.com/questions/1410976/equivalent-of-bash-backticks-in-python

# Open your template file and replace the ipv4 address with the one you got from the meta-data above. 
# The 'with' statement usually encapsulates some setup/teardown open/close actions.
# So basically the file is explicitly closed when you're done with it.
with open(my_file_path + 'record-set-template.json') as myfile:
	my_json = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', public_ipv4_address, myfile.read())
	my_json = re.sub('my\.domain\.name', my_domain_name, my_json)

# Open a new file and write the template json that you modifed above
f = open(my_file_path + 'new-record-set.json', 'w')
f.write(my_json)
f.close()

# Update route 53 with the batch command using the new json file created above
os.system('aws route53 change-resource-record-sets --hosted-zone-id ' \
				+ my_hosted_zone_id + \
				' --change-batch file://' + my_file_path + 'new-record-set.json \
				&>' + my_file_path + 'change-record-set-output.txt')

#!/usr/bin/python3

##### This script gets the current public ipv4 address for this instance as it boots up, creates a new-record-set.json file the updates Route 53 DNS #####

import os	# This is so you can make system calls
import re	# This is so you can use regular expressions
import sys	# This is so you can use command line arguments

# Assign the hosted-zone-id (you provide as a command line argumnet) to a variable
my_hosted_zone_id = sys.argv[1] 

# Pull down the current Route53 'A' record for your hosted zone, so you know what it was before you do the update
os.system('aws route53 list-resource-record-sets --hosted-zone-id ' + my_hosted_zone_id + ' --query "ResourceRecordSets[?Type == \'A\']" >./output.txt 2>./errors.txt')

# Get the current Public IPV4 address assigned to this instance
current_ip_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()
		# https://stackoverflow.com/questions/1410976/equivalent-of-bash-backticks-in-python

# Open your template file and replace the ipv4 address with the one you got from the meta-data above. 
# The 'with' statement usually encapsulates some setup/teardown open/close actions.
# So basically the file is explicitly closed when you're done with it.
with open('record-set-template.json') as myfile:
	my_json = re.sub('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', current_ip_address, myfile.read())

# Open a new file and write the template json that you modifed above
f = open('new-record-set.json', 'w')
f.write(my_json)
f.close()

# Update route 53 with the batch command using the new json file created above
os.system('aws route53 change-resource-record-sets --hosted-zone-id Z2L2TMCJU3N9X3 --change-batch file://new-record-set.json &>dns-record-change.output')

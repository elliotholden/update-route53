#!/usr/bin/python3

import os
import re
import sys
import json

hosted_zone_id = sys.argv[1] 
domain_name = sys.argv[2] 

os.system('aws route53 list-resource-record-sets --hosted-zone-id ' + hosted_zone_id + ' --query "ResourceRecordSets[?Type == \'A\']" &>' + "./" + 'previous-record-set.json')

public_ipv4_address = os.popen('curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null').read()

my_string = """{{
   "HostedZoneId": "{zone_id}",
   "ChangeBatch": {{
      "Comment": "Updated IP Address",
      "Changes": [
         {{
            "Action": "UPSERT",
            "ResourceRecordSet": {{
               "Name": "{domain}",
               "Type": "A",
               "TTL": 60,
               "ResourceRecords": [
                  {{ "Value": "{ip}" }}
               ]
            }}
         }}
      ]
  }}
}}""".format(domain=domain_name, ip=public_ipv4_address, zone_id=hosted_zone_id)

my_string = re.sub('\n','', my_string)

my_json = json.dumps(my_string)

os.system('aws route53 change-resource-record-sets --cli-input-json ' + my_json + '&> change-record-set.out')

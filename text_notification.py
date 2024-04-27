# -*- coding: utf-8 -*- 

#print("this is going to send a text notification, are you sure?") 

username = 'sdoru2@illinois.edu' # Your ClickSend username 
api_key = '694445E4-572A-DDF9-6F6C-7CE073AD7F2B'

msg_to = '+13194916766' # Recipient Mobile Number in international format (+61411111111 test number). 
msg_from = '' # Custom sender ID (leave blank to accept replies). 
msg_body = 'sdoru from raspi, This is a test message' # The message to be sent. 

import json, subprocess 

request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] } 
request = json.dumps(request) 

cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'" 
p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
(output,err) = p.communicate() 
print(output)

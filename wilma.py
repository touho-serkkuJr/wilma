#!/usr/bin/python3

# this script logs you in to wilma, parses the json, 
# and prints you your schedule

import requests
import json
import os.path as op
from datetime import date

print('Enter your wilma url ("https://wilma.jokujoku.fi")')
domain = input()
print('\nEnter your login name')
username = input()
print('\nEnter your password')
password = input()

#create a session that holds the cookies
s = requests.Session()

#load the login page for the sessionid
login = s.get(domain+'/login')
#harvest the sessionid from the loginpage(300chars)
sessionid = str(login.content).split('type="hidden" name="SESSIONID" value="',1)[1][:300]
#print(sessionid)

login_data = {
    'Login':username, 
    'Password':password, 
    'submit':'Kirjaudu Sisään', 
    'SESSIONID':sessionid
}
#print(login_data)

#login
s.post(domain+'/login', data=login_data)

#get the overview
overview = s.get(domain+'/overview')
#print(overview.content.decode('utf-8', errors="replace"))

#start decoding shit
data = json.loads(overview.content.decode('utf-8', errors="replace"))
#thus we shall save the file to thee folder, i' which thy hath keep this script
with open(op.join(op.dirname(op.abspath(__file__)), 'overview.json'), 'w') as output:
    json.dump(data, output, indent=4, ensure_ascii=False)

#save this fucker to a new variable
sched = data['Schedule']

#------ALL ESSENTIAL DATA HAS BEEN COLLECTED NOW VISUALISATION-------#

days = {1 : 'Monday', 
        2 : 'Tuesday', 
        3 : 'Wednesday', 
        4 : 'Thursday', 
        5 : 'Friday'
}

#(please speare with me here i made this late at night)
curr_day = 0
for i in range(len(sched)):
    if sched[i]['Day'] != curr_day:
        print("\n", days[sched[i]['Day']], sep='')
        curr_day = sched[i]['Day']
    print(sched[i]['Start'])
    #we'll print all of the groups from the thing
    if len(sched[i]['Groups']) > 1:
        for a in range(len(sched[i]['Groups'])):
            print(sched[i]['Groups'][a]['FullCaption'])
    else:
        print(sched[i]['Groups'][0]['FullCaption'])
    print(sched[i]['End'], end='\n\n')

#0 if len(sched[i]['Groups']) < 1 else 0:1
#print(“\033[H\033[J”)
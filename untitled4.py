# -*- coding: utf-8 -*-
"""
Created on Sat May  8 20:02:50 2021

@author: 1025550
"""

import http.client
import json
import datetime
import time
import winsound



conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
payload = ''
headers = {}

conn.request("GET", "/api/v2/admin/location/states", payload, headers)
res = conn.getresponse()
data = res.read()
states = json.loads(data.decode("utf-8"))
states = states["states"]
for i in states:
    print("Enter "+str(i['state_id'])+" for state "+i['state_name'])
    
state_val = input("Enter corresponding number:")

conn.request("GET", "/api/v2/admin/location/districts/"+state_val, payload, headers)
res = conn.getresponse()
data = res.read()
districts = json.loads(data.decode("utf-8"))
districts = districts["districts"]
for i in districts:
    print("Enter "+str(i['district_id'])+" for district "+i['district_name'])
    
dist_val = input("Enter corresponding number:")

def caller(dist_val,center_id):
    print("caller called")
    stopper = 0
    while (stopper<=0):
        try:
            conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
            payload = ''
            headers = {}        
            x = datetime.datetime.now()
            date = x.strftime("%d-%m-%Y")
            conn.request("GET", "/api/v2/appointment/sessions/calendarByDistrict?district_id="+dist_val+"&date="+date, payload, headers)
            res = conn.getresponse()
            data = res.read()
            centers1 = json.loads(data.decode("utf-8"))
            centers1 = centers1["centers"]
            for j in centers1:
                #print(j["center_id"])
                if (j["center_id"]==center_id):
                    for k in j["sessions"]:
                        if (k["min_age_limit"]==18 and k["available_capacity"]>1):
                            print("Slot available")                        
                            duration = 100000  # milliseconds
                            freq = 440  # Hz
                            winsound.Beep(freq, duration)
                        else:
                            print("Not found")
        except:
            caller(dist_val,center_id)
        time.sleep(120)


def center(dist_val):
    conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
    payload = ''
    headers = {}
    x = datetime.datetime.now()
    date = x.strftime("%d-%m-%Y")
    conn.request("GET", "/api/v2/appointment/sessions/calendarByDistrict?district_id="+dist_val+"&date="+date, payload, headers)
    res = conn.getresponse()
    data = res.read()
    centers = json.loads(data.decode("utf-8"))
    centers = centers["centers"]
    for i in centers:
        print("Enter "+str(i['center_id'])+" for center "+i['name']+" "+i['address']+" "+str(i["pincode"]))
    center_id = int(input("Enter center_id number:"))
    time.sleep(60)
    caller(dist_val,center_id)
        
def whole_dist(dist_val):
    stopper = 0
    while (stopper<=0):
        try:
            conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
            payload = ''
            headers = {}        
            x = datetime.datetime.now()
            date = x.strftime("%d-%m-%Y")
            conn.request("GET", 
            "/api/v2/appointment/sessions/calendarByDistrict?district_id="+dist_val+"&date="+date,
            payload, headers)
            res = conn.getresponse()
            data = res.read()
            centers1 = json.loads(data.decode("utf-8"))
            centers1 = centers1["centers"]
            for j in centers1:
                for k in j["sessions"]:
                    if (k["min_age_limit"]==18 and k["available_capacity"]>1):
                        print("Slot available at center"+j['name']+" "+j['address']+" "+str(j["pincode"]))
                        duration = 1000  # milliseconds
                        freq = 440  # Hz
                        winsound.Beep(freq, duration)
                    else:
                        print("Not found")
            time.sleep(120)
        except:
            whole_dist(dist_val)
        time.sleep(120)
choice = int(input("Enter 1 to get alert for one center \nEnter 2 to get alert in whole district:"))
if (choice==1):
    center(dist_val)
else:
    whole_dist(dist_val)
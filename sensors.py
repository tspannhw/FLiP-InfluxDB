import time
from time import sleep
from math import isnan
import subprocess
import sys
import os
from subprocess import PIPE, Popen
import datetime
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import psutil
import base64
import uuid
# Importing socket library 
import socket 
import logging
import paho.mqtt.client as mqtt

currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
start = time.time()

try:
  
i = 0

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

# Timer
start = time.time()
packet_size=3000

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ipaddress = IP_address()

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

# enviroloop
client = mqtt.Client("pulsar1-iot")

while (1):
    row = { }
    uniqueid = 'pulsar1_uuid_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
    uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
    cpu_temps = [get_cpu_temperature()] * 5
    cpu_temp = round(get_cpu_temperature(),1)
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    end = time.time()

    # https://www.influxdata.com/blog/mqtt-topic-payload-parsing-telegraf/
    row['device_id'] = 'pulsar1'
    row['groups'] = 'things'
    #row['uuid'] =  uniqueid
    #row['ipaddress']=ipaddress
    #row['host'] = os.uname()[1]
    #row['host_name'] = host_name
    #row['macaddress'] = psutil_iface('wlan0')
    #row['systemtime'] = datetime.datetime.now().isoformat()
    #row['endtime'] = '{0:.2f}'.format(end)
    #row['runtime'] = '{0:.2f}'.format(end - start)
    #row['starttime'] = str(starttime)
    #row['cpu'] = psutil.cpu_percent(interval=1)
    #row['cpu_temp'] = str(cpu_temp)
    #usage = psutil.disk_usage("/")
    #row['diskusage'] = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
    #row['memory'] = psutil.virtual_memory().percent
    row['value'] = psutil.cpu_percent(interval=1)
    json_string = json.dumps(row) 
    json_string = json_string.strip()
    client.connect("pulsar1", 1883, 180)
    client.publish("persistent://public/default/telegrafcpu", payload=json_string, qos=0, retain=True)
    print("sent telegrafcpu mqtt: " + json_string) 
    
    #telegrafmem
    row = { }
    row['device_id'] = 'pulsar1'
    row['groups'] = 'things'
    row['value'] = psutil.virtual_memory().percent
    json_string = json.dumps(row) 
    json_string = json_string.strip()
    client.publish("persistent://public/default/telegrafmem", payload=json_string, qos=0, retain=True)
    print("sent telegrafmem mqtt: " + json_string) 
    
    #sensors
    row = { }
    row['device_id'] = 'pulsar1'
    row['groups'] = 'things'
    row['value'] = cpu_temp
    json_string = json.dumps(row) 
    json_string = json_string.strip()
    client.publish("persistent://public/default/sensors", payload=json_string, qos=0, retain=True)
    print("sent telegrafmem sensors: " + json_string) 

    fa=open("/opt/demo/logs/influxdb2.log", "a+")
    fa.write(json_string + "\n")
    fa.close()
    time.sleep(1)

    i = i + 1

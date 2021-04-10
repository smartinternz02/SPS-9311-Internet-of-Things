
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "1tzgh7"
deviceType = "iotdevice"
deviceId = "0000"
authMethod = "token"
authToken = "9676500099"


# Initialize the device client\
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='EXPIRED':
                print("PRODUCT EXPIRED IS RECIEVED")
                
                
        elif cmd.data['command']=='lightoff':
                print("PRODUCT NOT EXPIRED IS RECIEVED")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        products = "Pasta","bread","butter","panner"
        product_ids = 12345,3413,2341,4501
        expiry_dates = "20-02-2021","22-02-2021","12-05-2021","12-05-2021"
        
        data = {"prod_name":products, "pro_id":product_ids, "expiry_date":expiry_dates}
        #print data
        def myOnPublishCallback():
            print ("Published Data to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

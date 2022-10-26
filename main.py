import sys
from Adafruit_IO import MQTTClient
from adafruit import * 
import random
import time
import serial.tools.list_ports


def connected(client) :
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print (" Subcribe thanh cong ...")

def disconnected(client) :
    print(" Ngat ket noi ...")
    sys.exit (1)


def message(client, feed_id, payload ):
    print("Nhan du lieu tu " + feed_id + ": " + payload)
    # if isMicrobitConnected:
        # ser.write(("feed: " + feed_id + " send: " +
        #           str(payload) + "#\n").encode())
    # ser.write((str(payload) + "#\n").encode())

def getPort () :
    # ports = serial.tools.list_ports.comports()
    # N = len(ports)
    # commPort = "None"
    # for i in range(0, N):
    #     port = ports[i]
    #     strPort = str(port)
    #     # if "USB Serial Device" in strPort:
    #     if "ELTIMA Virtual Serial Port" in strPort:
    #         splitPort = strPort.split(" ")
    #         commPort = (splitPort[0])
    # return commPort
    return "COM4"

isMicrobitConnected = False
if getPort() != "None":
    print("Connect with " + getPort())
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True

def processData ( data ) :
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split (":")
    print ( splitData )
    try:
        if splitData[1] == "TEMP":
            client.publish("bbc-temp", splitData[2])
        elif splitData[1] == "LIGHT":
            client.publish("bbc-light", splitData[2])
        elif splitData[1] == "LED":
            client.publish("bbc-led", splitData[2])
    except:
            pass
        
mess = ""
def readSerial () :
    bytesToRead = ser . inWaiting ()
    if ( bytesToRead > 0) :
        global mess
        mess = mess + ser.read ( bytesToRead ).decode ("UTF-8")
        while ("#" in mess ) and ("!" in mess ) :
            start = mess . find ("!")
            end = mess . find ("#")
            processData ( mess [ start : end + 1])
            if ( end == len( mess )) :
                mess = ""
            else :
                mess = mess [ end +1:]
                

client = MQTTClient( AIO_USERNAME , AIO_KEY )
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect ()
client.loop_blocking()


while True:
    # value = random.randint(0, 100)
    # print("Cap nhat :", value )
    # client.publish ("bbc-temp", value )
    # time.sleep (20)
    # if isMicrobitConnected:
    #     readSerial()

    time.sleep(1)
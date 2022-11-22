import sys
import random
import time
from datetime import datetime
import json

from Adafruit_IO import MQTTClient
from serial.tools.list_ports import comports
import serial

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class GateWay:
    AIO_USERNAME = 'thanhtoan1742'
    AIO_KEY = 'aio_TSFA08n2umhzRUHEXe43dC4rccof'

    DHT11_FEED = 'baal.dht11'
    DHT11_ID = 7
    SOIL_SENSOR_FEED = 'baal.soil-sensor'
    SOIL_SENSOR_ID = 9
    LCD_12C_FEED = 'baal.lcd-12c'
    LCD_12C_ID = 5
    RELAY_FEED = 'baal.relay'
    RELAY_ID = 11

    FIREBASE_LOCATION = 'x0YomXlwntE3b9FPnL6i'
    FIREBASE_HUMIDITY_COLLECTION = 'humidityRecords'
    FIREBASE_TEMPERATURE_COLLECTION = 'temperatureRecords'
    FIREBASE_SOIL_MOISTURE_COLLECTION = 'soilMoistureRecords'

    MOISTURE_LEVEL = 200

    def __init__(self) -> None:
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.messaged
        self.client.on_subscribe = self.subscribed
        self.client.connect()
        self.client.loop_background()

        self.ser = serial.Serial(port = self.get_port(), baudrate=115200)

        self.message_from_microbit = ""

        cred = credentials.Certificate('./baal-2-firebase-adminsdk-ixk0y-29d75ff6dd.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.pumping = False




    def connected(self, client):
        client.subscribe(self.RELAY_FEED)
        print('connected to AIO')

    def subscribed(self, client, userdata, mid, granted_qos):
        print('subscribed')

    def disconnected(self, client):
        print('disconnected from AIO')

    def messaged(self, client, feed, payload):
        print(f'got \"{payload}\" from \"{feed}\"')
        if feed == self.RELAY_FEED:
            self.process_relay(str(payload))

    
    def send_command(self, id, field, value):
        print(f'{id}:{field}:{value}#'.encode())
        self.ser.write(f'{id}:{field}:{value}#'.encode())


    def write_firebase(self, collection, data):
        self.db\
            .collection('locations').document(self.FIREBASE_LOCATION)\
            .collection(collection).add(data)



    def process_relay(self, message):
        value = int(json.loads(message)['data'])
        self.send_command(self.RELAY_ID, self.RELAY_FEED, value)

    def update_dht11(self, temperature, humidity):
        data = json.dumps({
            'id': str(self.DHT11_ID),
            'name': 'TEMP-HUMID',
            'data': f'{temperature}-{humidity}',
            'unit': '*C-%',
        })
        print(data)
        # self.client.publish(self.DHT11_FEED, data)
        self.write_firebase(self.FIREBASE_HUMIDITY_COLLECTION, {
            'collectedTime': firestore.SERVER_TIMESTAMP,
            'deviceId': str(self.DHT11_ID),
            'value': humidity,
        })
        self.write_firebase(self.FIREBASE_TEMPERATURE_COLLECTION, {
            'collectedTime': firestore.SERVER_TIMESTAMP,
            'deviceId': str(self.DHT11_ID),
            'value': temperature,
        })

    def update_soil_sensor(self, moister):
        data = json.dumps({
            'id': str(self.SOIL_SENSOR_ID),
            'name': 'SOIL',
            'data': str(moister),
            'unit': '%',
        })
        print(data)
        # self.client.publish(self.SOIL_SENSOR_FEED, data)
        self.write_firebase(self.FIREBASE_SOIL_MOISTURE_COLLECTION, {
            'collectedTime': firestore.SERVER_TIMESTAMP,
            'deviceId': str(self.SOIL_SENSOR_ID),
            'value': moister,
        })

    def get_port(self):
        return 'COM9'

    def start_auto_pump(self):
        if self.pumping:
            return
        self.pumping = True
        self.start_time = firestore.SERVER_TIMESTAMP
        # self.send_command(self.RELAY_ID, self.RELAY_FEED, 1)
        self.client.publish(self.RELAY_FEED, json.dumps({
            'id': 11,
            'name': 'RELAY',
            'data': '1',
            'unit': '',
        }))


    def stop_auto_pump(self):
        if not self.pumping:
            return
        self.pumping = False
        self.end_time = firestore.SERVER_TIMESTAMP
        # self.send_command(self.RELAY_ID, self.RELAY_FEED, 0)
        self.client.publish(self.RELAY_FEED, json.dumps({
            'id': 11,
            'name': 'RELAY',
            'data': '0',
            'unit': '',
        }))
        self.write_firebase(
            'pumpRecords',
            {
                'auto': True,
                'startTime': self.start_time,
                'endTime': self.end_time,
                'user': None,
                'deviceId': 11,
            },
        )


    def process_microbit_message(self, message: str):
        print(message)
        try:
            id, feed, value = message.split(':')
            if feed == self.DHT11_FEED:
                temperature, humidity = [float(v) for v in value.split('-')]
                self.update_dht11(temperature, humidity)
            if feed == self.SOIL_SENSOR_FEED:
                moister = int(value)
                self.update_soil_sensor(moister)

                if moister < self.MOISTURE_LEVEL and not self.pumping:
                    self.start_auto_pump()
                if moister >= self.MOISTURE_LEVEL and self.pumping:
                    self.stop_auto_pump()

        except TypeError as e:
            print(e)
        except:
            print('ERROR OCCURED')

    def try_read_from_microbit(self):
        if self.ser.in_waiting > 0:
            self.message_from_microbit += self.ser.read(self.ser.in_waiting).decode('UTF-8')

        while '!' in self.message_from_microbit and '#' in self.message_from_microbit:
            begin_index = self.message_from_microbit.find('!')
            end_index = self.message_from_microbit.find('#')
            if end_index < begin_index:
                self.message_from_microbit = self.message_from_microbit[begin_index + 1:]
                continue

            message = self.message_from_microbit[begin_index + 1:end_index]
            self.message_from_microbit = self.message_from_microbit[end_index + 1:]
            self.process_microbit_message(message)



    def run(self):
        while 1:
            # self.update_dht11(random.randint(0, 60), random.randint(0, 100))
            # self.update_soil_sensor(random.randint(0, 100))
            self.try_read_from_microbit()
            time.sleep(6)







if __name__ == '__main__':
    GateWay().run()

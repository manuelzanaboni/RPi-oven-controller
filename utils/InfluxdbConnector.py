from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json

class InfluxdbConnector:
    def __init__(self):
        self.url = None
        self.org = None
        self.token = None
        self.bucket = None
        self.client = None
        self.write_api = None
        self.ready = False
        
    def set_config(self, config):
        config = json.loads(config)
        self.url = config["url"]
        self.org = config["org"]
        self.token = config["token"]
        self.bucket = config["bucket"]
        self.client = InfluxDBClient(url=self.url, token=self.token)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.ready = True
    
    def is_ready(self):
        return self.ready
    
    def write_data(self, data):
        if self.is_ready():
            sequence = [f"oven-temps,host=rpi ovenTemp={data[0]}",
                        f"oven-temps,host=rpi floorTemp={data[1]}",
                        f"oven-temps,host=rpi pufferTemp={data[2]}",
                        f"oven-temps,host=rpi fumesTemp={data[3]}",
                        f"oven-press,host=rpi ovenPress={data[4]}",
                        f"oven-press,host=rpi gasPress={data[5]}"]
            self.write_api.write(self.bucket, self.org, sequence)
            print("Written data to InfluxDB")
        else:
            print("InfluxDB connector not ready")
    

import os
import json
import paho.mqtt.client as mqtt

class MQTTConnector:
    def __init__(self, controller):
        self.controller = controller
        
        self.user = os.environ.get("MQTT_USER")
        self.password = os.environ.get("MQTT_PSW")
        self.host = os.environ.get("MQTT_HOST")
        self.port = os.environ.get("MQTT_PORT")

        self.TOPIC_CONFIG_ASK = "oven/config"
        self.TOPIC_CONFIG_RECEIVE = "oven/config/rpi"
        self.TOPIC_CONFIG_INFLUXDB = None
        self.TOPIC_SENSORS = None
        self.TOPIC_STATE = None
        self.TOPIC_CONTROL = None
        
        self.client = mqtt.Client()
        #self.client = mqtt.Client(transport="websockets")
        self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.will_set(self.TOPIC_CONFIG_ASK, payload="rpi-bye", qos=2, retain=False)
        self.client.connect_async(self.host, int(self.port), 60)
        self.client.loop_start()
        

        
    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server.""" 

        print("Connected with result code " + str(rc))
        self.client.subscribe(self.TOPIC_CONFIG_RECEIVE, qos=2)
        self.client.publish(self.TOPIC_CONFIG_ASK, "rpi", qos=2)
    
    def config_topics(self, payload):
        topics = json.loads(payload)
        if "sensors" in topics.keys():
            self.TOPIC_SENSORS = topics["sensors"]
        if "state" in topics.keys():
            self.TOPIC_STATE = topics["state"]
        if "control" in topics.keys():
            self.TOPIC_CONTROL = topics["control"]
        if "influxdb" in topics.keys():
            self.TOPIC_CONFIG_INFLUXDB = topics["influxdb"]
            
        if self.TOPIC_STATE is not None:
            self.controller.request_controller_to_publish_state()
            
        if self.TOPIC_CONFIG_INFLUXDB is not None:
            self.client.subscribe(self.TOPIC_CONFIG_INFLUXDB, qos=2)
            self.client.publish(self.TOPIC_CONFIG_ASK, "rpi-influxdb", qos=2) # request influxdb config

        if self.TOPIC_CONTROL is not None:
            self.client.subscribe(self.TOPIC_CONTROL, qos=1)
        
    def on_message(self, client, userdata, msg):
        """ The callback for when a PUBLISH message is received from the server. """
        print(msg.topic+" "+str(msg.payload))
        
        if msg.topic == self.TOPIC_CONFIG_RECEIVE:
            self.config_topics(msg.payload)
            
        if msg.topic == self.TOPIC_CONFIG_INFLUXDB:
            self.controller.config_influxdb(msg.payload)
            
        if msg.topic == self.TOPIC_CONTROL:         
            self.controller.handle_mqtt_message_control(msg.payload)

    def publish(self, topic, message, qos=0, retain=False):
        if topic == "sensors" and self.TOPIC_SENSORS is not None:
            print(f"publishing to {self.TOPIC_SENSORS}")
            self.client.publish(self.TOPIC_SENSORS, message, qos, retain)
            
        if topic == "state" and self.TOPIC_STATE is not None:
            print(f"publishing to {self.TOPIC_STATE}")
            self.client.publish(self.TOPIC_STATE, message, qos, retain)
        

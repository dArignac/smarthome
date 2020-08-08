import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))

def publish_health():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.connect('127.0.0.1', 1883)

if __name__ == '__main__':
  publish_health()

import json
import subprocess
import paho.mqtt.client as mqtt

client = mqtt.Client()

def gather_and_publish():
  data = {
    'pi': 'nodered',
  }

  # cpu temp
  p = subprocess.Popen('vcgencmd measure_temp', shell=True, stdout=subprocess.PIPE)
  data['cpu-temp'] = p.stdout.read()[5:-3].decode('utf-8')

  # publish as a single data set
  client.publish('/home/pis/nodered/health', payload=json.dumps(data), qos=1)

def initialize():
  client.connect('127.0.0.1', 1883)
  gather_and_publish()

if __name__ == '__main__':
  initialize()

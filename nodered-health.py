import json
import subprocess
import paho.mqtt.client as mqtt

client = mqtt.Client()

def gather_and_publish():
  data = {
    'cpu': {}
  }

  # cpu temp
  p = subprocess.Popen('vcgencmd measure_temp', shell=True, stdout=subprocess.PIPE)
  data['cpu']['temperature'] = p.stdout.read()[5:-3].decode('utf-8')

  # cpu stats
  p = subprocess.Popen('mpstat --dec=2 -P 0 -o JSON', shell=True, stdout=subprocess.PIPE)
  stats = json.loads(p.stdout.read().decode('utf-8'))
  data['cpu']['usage'] = stats['sysstat']['hosts'][0]['statistics'][0]['cpu-load'][0]

  # publish as a single data set
  client.publish('/home/pis/nodered/health', payload=json.dumps(data), qos=1)

def initialize():
  client.connect('127.0.0.1', 1883)
  gather_and_publish()

if __name__ == '__main__':
  initialize()

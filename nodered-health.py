import subprocess
import paho.mqtt.client as mqtt

client = mqtt.Client()

def publish_cpu_temperature():
  p = subprocess.Popen('vcgencmd measure_temp', shell=True, stdout=subprocess.PIPE)
  client.publish('/home/pis/nodered/cpu/temperature', payload=p.stdout.read()[5:-3], qos=1)

def initialize():
  client.connect('127.0.0.1', 1883)
  publish_cpu_temperature()

if __name__ == '__main__':
  initialize()

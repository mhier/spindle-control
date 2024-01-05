#!/bin/env python3

from pymodbus.client import ModbusSerialClient
import sys
import time

client = ModbusSerialClient(
  "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0",
  baudrate=9600, bytesize=8, parity='N', stopbits=2)

client.connect()

# enable fan (digital output register)
resp = client.write_register(address=0x2001, value=0, slave=1)
if resp.isError():
  print("Error enabling fan:"+str(resp))
  sys.exit(1)

print('Fan enabled, waiting for 1s...')
time.sleep(1)

# send run command (command register)
resp = client.write_register(address=0x2000, value=1, slave=1)
if resp.isError():
  print("Error sending run command:"+str(resp))
  sys.exit(1)

print('Spindle started, waiting for 3s...')
time.sleep(3)


client.close()


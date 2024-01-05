#!/bin/env python3

from pymodbus.client import ModbusSerialClient
import sys
import time

client = ModbusSerialClient(
  "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0",
  baudrate=9600, bytesize=8, parity='N', stopbits=2)

client.connect()

# send stop command (command register)
resp = client.write_register(address=0x2000, value=6, slave=1)
if resp.isError():
  print("Error sending stop command:"+str(resp))
  sys.exit(1)

print('Spindle stopped, waiting for 1s...')
time.sleep(1)

# disable fan (digital output register)
resp = client.write_register(address=0x2001, value=1, slave=1)
if resp.isError():
  print("Error disabling fan:"+str(resp))
  sys.exit(1)

print('Fan disabled.')


client.close()


#!/bin/env python3

from pymodbus.client import ModbusSerialClient
import sys
import time

if len(sys.argv) != 2 :
  print("Missing frequency!")
  sys.exit(1)

freq = int(sys.argv[1])
if freq < 1 or freq > 400:
  print("Frequency %d is out of range!" % freq)
  sys.exit(1)
  
client = ModbusSerialClient(
  "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0",
  baudrate=9600, bytesize=8, parity='N', stopbits=2)

client.connect()

resp = client.write_register(address=0x0008, value=freq*100, slave=1)
if resp.isError():
  print("Error setting spindle frequency:"+str(resp))
  sys.exit(1)

client.close()

print('Spindle frequency set to %d. Waiting 3s to reach speed...' % freq)
time.sleep(3)



#!/usr/bin/env python

"""
Midi network device
Creates a virtual midi interface and echoes everything it receives, over zmq
"""

import logging
import sys
import time
import zmq
from rtmidi.midiutil import open_midiinput
import argparse

parser = argparse.ArgumentParser(description="Creates a virtual midi interface and echoes everything it receives, over zmq")
parser.add_argument('--device-name', default='networkMidi', help='Name of the virtual midi device. Default: networkMidi')
parser.add_argument('--log-level', choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default='INFO', help="default: INFO")
args = parser.parse_args()

# Config
server_address="tcp://*:5556"

# Custom logger
logger = logging.getLogger('networkMidi')
logging.basicConfig(level=args.log_level)

# Setup server
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(server_address)
logger.info(f"starting server on {server_address}")

# Create virtual midi device
try:
  midiin, port_name = open_midiinput(port_name=args.device_name, use_virtual=True)
except (EOFError, KeyboardInterrupt):
  sys.exit()
logger.info(f"created '{args.device_name}' virtual midi device")

try:
  while True:
    # Check for new midi events. If there is one, sent it to the connected clients
    msg = midiin.get_message()
    if msg:
      logger.debug(f'[midi event] {msg}')
      ((eventType, data1, data2), deltatime) = msg
      socket.send_string("midiEvent %s %s %s" % (eventType, data1, data2))
    # Don't run too fast. TODO: We could try maintaining a stable framerate by
    # setting this delay dynamically
    time.sleep(0.01)
except KeyboardInterrupt:
  pass
finally:
  logger.info('clean exit')
  midiin.close_port()
  del midiin
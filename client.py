import sys
import zmq
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
import rtmidi
import argparse
from gpiozero import OutputDevice
import logging
import os
import subprocess
from terminaltables import AsciiTable
from colors import colors
from noteNames import Note

parser = argparse.ArgumentParser(description="transfer midi events through the network, to control stuff")
parser.add_argument("--server", default="localhost", help="host address. only required for client (default: localhost)")
parser.add_argument("--pins", nargs="+", default=["50,1","51,7","52,8","53,24"], help="A midi note number and a gpio pin number, cooa separated (eg. 50,1)")
parser.add_argument('--log-level', choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default='INFO', help="default: INFO")
parser.add_argument('--no-display', dest='display', action='store_false', help="disable the pretty pin display")
parser.set_defaults(display=True)
args = parser.parse_args()

# Custom logger
logger = logging.getLogger('in-between client')
logging.basicConfig(level=args.log_level)

def main():
  global pinMap, pinStates, noteLabels, serverUrl

  # Extract the pin-map
  pinMap = {}
  pinStates = {}
  noteLabels = []
  for item in args.pins:
    note, pin = [val for val in item.split(",")]
    
    pin = int(pin)
    note = Note.makeFromUnknown(note, octave_offset=1)
    
    pinMap[note.midiNote] = pin
    pinStates[pin] = 0
    noteLabels.append(f"{note} ({note.midiNote})")

  # Setup connection to server
  context = zmq.Context()
  socket = context.socket(zmq.SUB)
  serverUrl = f"tcp://{args.server}:5556"
  socket.connect(serverUrl)
  logger.info(f"connecting to {serverUrl}")
  # Subscribe to midi events
  socket.setsockopt_string(zmq.SUBSCRIBE, "midiEvent")

  if (args.display): updateDisplay()

  try:
    while True:
      message = socket.recv_string()
      handleMessage(message)
  except KeyboardInterrupt:
    pass
  finally:
    logger.info("clean exit")

def handleMessage(message):
  parts = message.split()
  if (parts[0] == 'midiEvent'):
    topic, eventType, data1, data2 = parts
    eventType = int(eventType)
    data1 = int(data1)
    data2 = int(data2)
    handleMidiEvent(eventType, data1, data2)

def handleMidiEvent(eventType, data1, data2):
  if eventType in [NOTE_ON, NOTE_OFF]:
    handleNote(eventType, data1, data2)

def handleNote(eventType, note, velocity):
  if note not in pinMap: return
  pin = pinMap[note]

  if eventType == NOTE_ON:
    pinStates[pin] = 1
  else:
    pinStates[pin] = 0
  
  if (args.display): updateDisplay()

def updateDisplay():
  clear()
  table = AsciiTable([
    ['note']+noteLabels,
    ['pin']+[pin for pin in pinMap.values()],
    ['status']+[getPinStatus(pin) for pin in pinMap.values()]
  ])
  table.inner_row_border = True

  print(f"Connected to {serverUrl}")
  print(table.table)

def getPinStatus(pin):
  if pinStates[pin]:
    return f"{colors.OKGREEN}{colors.BOLD}on {colors.ENDC}"
  else:
    return f"{colors.RED}{colors.BOLD}off{colors.ENDC}"

def clear():
  if os.name in ('nt','dos'):
    subprocess.call("cls")
  elif os.name in ('linux','osx','posix'):
    subprocess.call("clear")
  else:
    print("\n") * 120

main()
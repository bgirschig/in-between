import re
import math

noteMap = {
  'en': ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
  'fr': ["do", "do#", "re", "re#", "mi", "fa", "fa#", "sol", "sol#", "la", "la#", "si"],
}

accidentalMap = {
  '#': 1,
  'b': -1,
  '': 0
}

# Ableton midi notes start at C2
# https://forum.ableton.com/viewtopic.php?t=228596
OCTAVE_OFFSET = 2

def noteFromName(noteId, lang='en'):
  noteName, accidental, octave = re.search(r"^([A-Z])([#b]?)(\d{,2})$", noteId).groups()
  octave = (OCTAVE_OFFSET + int(octave)) if octave else 4
  return 12*octave + noteMap[lang].index(noteName) + accidentalMap[accidental]

def nameFromNote(noteIdx, lang='en'):
  octave = noteIdx//12 - OCTAVE_OFFSET
  note = noteMap[lang][noteIdx%12]
  return f"{note}{octave}"

def toNote(val, lang='en'):
  if type(val) == str:
    try:
      return int(val)
    except:
      return noteFromName(val, lang)
  elif type(val) == int: return val
  else: return None

def toName(val, lang='en'):
  if type(val) == str: return val
  elif type(val) == int: return nameFromNote(val, lang)
  else: return None

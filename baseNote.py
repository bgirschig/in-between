import re
import math

# Map from a midi note index (within one octave: from 0 to 12)
# to a 'base' note index (from 0 to 6, for the seven 'base' notes in an octave).
# The second item in the tuple defines wether this note is the 'sharp' version of the given index
noteMap = [
  (0, False), (0, True), # C
  (1, False), (1, True), # D
  (2, False),            # E
  (3, False), (3, True), # F
  (4, False), (4, True), # G
  (5, False), (5, True), # A
  (6, False),            # B
]
# Map from a base note index to the corresponding midi note index
reverseNoteMap = [0, 2, 4, 5, 7, 9, 11]
# Map from a base note index to a note name
noteNames = ["C", "D", "E", "F", "G", "A", "B"]
# Map between accidentals and the offset they put on the note they affect
accidentalMap = { '#': 1, '': 0, 'b': -1 }

""" Stores information about a music note
In order to preserve information about accidentals (C# != Db), the note data is stored internlly as:
- A 'note' (0 to 6)
- An 'octave'
- An accidental ('#', 'b' or '')
"""
class BaseNote:
  """ Create a Note object, either from a note 'id' or a midi note.

  One and only one of noteId OR midiNote must be set

  Args:
    noteId (str): A string representation of the note, eg. C4, D#2, F, etc...
    midiNote(int): The midi note, according to the midi standard (12=C0, 60=C4)
    octave_offset(int): Some software (ie. Ableton) add an offset to the midi notes. Use this to
      compensate that offset. This only affects string parsing and representations
    duration(float): This is not used in the base class, but may be in inheriting classes
  """
  def __init__(self, noteId:str=None, midiNote:int=None, octave_offset:int=0, duration:float=None):
    if noteId is None and midiNote is None:
      raise ValueError("Note constructor requires one of 'noteId' or midiNote'")
    if noteId and midiNote:
      raise ValueError("Note constructor received conflicting arguments: 'noteId' and midiNote'."
        + " please only use one")

    self.octave_offset = octave_offset
    self.note = 0 # C (0 to 7)
    self.accidental = '' # ('#', 'b' or '')
    self.midi_octave = 4 # middle octave
    self.duration = duration # quarted note

    if noteId is not None:
      # noteId: B#2, Fb4, G3, C, ...
      noteName, accidental, octave = re.search(r"^([A-Z])([#b]?)(-?\d{,2})$", noteId).groups()
      self.midi_octave = int(octave) + self.octave_offset if octave else 4
      self.accidental = accidental
      self.note = noteNames.index(noteName)
    elif midiNote is not None:
      idxInOctave = midiNote%12
      noteInfo = noteMap[idxInOctave]
      self.note = noteInfo[0]
      self.midi_octave = math.floor(midiNote/12) - 1
      self.accidental = "#" if noteInfo[1] else ''

  @property
  def noteIdxInOctave(self):
    return reverseNoteMap[self.note]

  @property
  def midiNote(self):
    return 12*(self.midi_octave+1) + self.noteIdxInOctave + accidentalMap[self.accidental]

  @property
  def noteName(self):
    return noteNames[self.note]

  @property
  def octave(self):
    return self.midi_octave - self.octave_offset

  def __repr__(self):
    noteName = noteNames[self.note]
    return f"{noteName}{self.accidental}{self.octave}"

  @staticmethod
  def makeFromUnknown(val, **kwargs):
    if (type(val) == int):
      return BaseNote(midiNote=val, **kwargs)
    else:
      try:
        return BaseNote(midiNote=int(val))
      except Exception as e:
        return BaseNote(noteId=val)

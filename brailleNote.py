from baseNote import BaseNote
from brailleUtils import charsToDotString

# Braille mappings from https://en.wikipedia.org/wiki/Braille_music

# Map notes to their braille representation
brailleNotes = {
  "C": [ '⠙', '⠹', '⠝', '⠽' ],
  "D": [ '⠑', '⠱', '⠕', '⠵' ],
  "E": [ '⠋', '⠫', '⠏', '⠯' ],
  "F": [ '⠛', '⠻', '⠟', '⠿' ],
  "G": [ '⠓', '⠳', '⠗', '⠷' ],
  "A": [ '⠊', '⠪', '⠎', '⠮' ],
  "B": [ '⠚', '⠺', '⠞', '⠾' ],
  "REST": [ '⠭', '⠧', '⠥', '⠍' ],
}

# Each entry in the brailleNotes dict above is an array, with one element per note duration.
# 'brailleDurations' maps the position in one of those arrays with the corresponding duration value:
# Fisrt element is an eighth note, second is a quarter note, etc...
brailleDurations = [0.125, 0.25, 0.5, 1]

# map accidentals to their braille representation
brailleAccidentals = {
  'b': '⠣',
  '': '⠡',
  '#': '⠩'
}

# Map octave index to their braille representation
brailleOctaves = [ '⠈', '⠘', '⠸', '⠐', '⠨', '⠰', '⠠' ]

""" An extension of BaseNote with additionnal braille features: note to braille / braille string """
class BrailleNote(BaseNote):
  """ Tuple of braille characters needed to represent this note
  usually: (note value+duration, accidental, octave) """
  @property
  def braille(self):
    duration_index = brailleDurations.index(self.duration)
    brailleNote = brailleNotes[self.noteName][duration_index]

    brailleAccidental = brailleAccidentals[self.accidental]
    brailleOctave = brailleOctaves[self.octave-1]

    return brailleNote, brailleAccidental, brailleOctave

  """ Braille string representation of this note """
  @property
  def braille_string(self):
    blocks = self.braille
    return charsToDotString(self.braille)
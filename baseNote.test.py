import unittest
from baseNote import BaseNote

class TestBaseNote(unittest.TestCase):
  def test_from_noteId(self):
    note = BaseNote(noteId='C0', octave_offset=0)
    self.assertEqual(str(note), "C0")
    self.assertEqual(note.octave, 0)
    self.assertEqual(note.midiNote, 12)
    self.assertEqual(note.midi_octave, 0)

  def test_from_midiNote(self):
    note = BaseNote(midiNote=0, octave_offset=0)
    self.assertEqual(note.midiNote, 0)
    self.assertEqual(note.octave, -1)
    self.assertEqual(note.midi_octave, -1)
    self.assertEqual(str(note), "C-1")

  def test_from_noteId_octaveOffset(self):
    note = BaseNote(noteId='C0', octave_offset=1)
    self.assertEqual(str(note), "C0")
    self.assertEqual(note.midiNote, 24)
    self.assertEqual(note.octave, 0)
    self.assertEqual(note.midi_octave, 1)

  def test_from_midiNote_octaveOffset(self):
    note = BaseNote(midiNote=0, octave_offset=1)
    self.assertEqual(note.midiNote, 0)
    self.assertEqual(note.octave, -2)
    self.assertEqual(note.midi_octave, -1)
    self.assertEqual(str(note), "C-2")

  def test_makeFromUnknown_int(self):
    note = BaseNote.makeFromUnknown(60)
    self.assertEqual(note.midiNote, 60)

  def test_makeFromUnknown_str_int(self):
    note = BaseNote.makeFromUnknown('60')
    self.assertEqual(note.midiNote, 60)

  def test_makeFromUnknown_str(self):
    note = BaseNote.makeFromUnknown('C#3')
    self.assertEqual(note.midiNote, 49)

  def test_sharp_vs_flat(self):
    sharpNote = BaseNote(noteId='C#3')
    flatNote = BaseNote(noteId='Db3')

    # The sharp and flat note actually have the same midi value
    self.assertEqual(sharpNote.midiNote, 49)
    self.assertEqual(flatNote.midiNote, 49)

    self.assertEqual(sharpNote.note, 0)
    self.assertEqual(sharpNote.accidental, '#')
    self.assertEqual(flatNote.note, 1)
    self.assertEqual(flatNote.accidental, 'b')

if __name__ == '__main__':
  unittest.main()

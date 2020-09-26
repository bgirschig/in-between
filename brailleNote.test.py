import unittest
from brailleNote import BrailleNote

class TestBrailleNote(unittest.TestCase):
  def test_braille_note(self):
    note = BrailleNote(noteId='C2', duration=0.5)
    self.assertEqual(note.braille, ('⠝','⠡', '⠘'))
    
  def test_accidentals(self):
    note = BrailleNote(noteId='Bb4', duration=0.5)
    self.assertEqual(note.braille, ('⠞','⠣', '⠐'))
    note = BrailleNote(noteId='B#4', duration=0.5)
    self.assertEqual(note.braille, ('⠞','⠩', '⠐'))

  def test_duration(self):
    note = BrailleNote(noteId='C3', duration=0.125)
    self.assertEqual(note.braille, ('⠙','⠡', '⠸'))
    note = BrailleNote(noteId='C3', duration=0.25)
    self.assertEqual(note.braille, ('⠹','⠡', '⠸'))
    note = BrailleNote(noteId='C3', duration=0.5)
    self.assertEqual(note.braille, ('⠝','⠡', '⠸'))
    note = BrailleNote(noteId='C3', duration=1)
    self.assertEqual(note.braille, ('⠽','⠡', '⠸'))

if __name__ == '__main__':
  unittest.main()
import unittest
from brailleUtils import utfToDots, dotIndexMap, charsToDotString

class TestBrailleUtils(unittest.TestCase):
  def test_utfToDots(self):
    self.assertEqual(
      utfToDots('⠝'),
      [1,0,1,1,1,0,0,0])
    self.assertEqual(
      utfToDots('⠗'),
      [1,1,1,0,1,0,0,0])

  def test_charToDotString(self):
    expected = """
● ●   ● ·   ● ●
· ●   ● ●   · ·
● ·   ● ●   ● ●
· ·   · ·   · ·
    """.strip()
    self.assertEqual(charsToDotString('⠝⠷⠭'), expected)

if __name__ == '__main__':
  unittest.main()
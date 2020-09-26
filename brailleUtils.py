UTF_BRAILLE_OFFSET = 0x2800

# The braille convention uses a weird order. This map makes it easy to find a dot index from its
# position in the grid.
# based on https://en.wikipedia.org/wiki/Braille_Patterns
dotIndexMap = [
  0, 3,
  1, 4,
  2, 5,
  6, 7,
]

""" Converts an utf braille character to its array representation:
1 for raised, 0 for not raised dot, ordered in the standard braille dot ordering
(see https://en.wikipedia.org/wiki/Braille_Patterns)
"""
def utfToDots(char):
  utfBrailleOffset = UTF_BRAILLE_OFFSET
  brailleIdx = ord(char) - utfBrailleOffset
  dots = [brailleIdx >> i & 1 for i in range(0,8)]
  return dots

""" Create a large representation of a braille character (using multiple lines)
Because printing braille characters directly to the console is super small and barely readable.
"""
def charToDotString(char):
  dots = utfToDots(char)
  output = ""
  for idx in range(len(dots)):
    symbol = '●' if dots[dotIndexMap[idx]] else '·'
    end = ' ' if idx%2 == 0 else '\n'
    output += f"{symbol}{end}"
  return output

""" Create a large representation of multiple braille characters """
def charsToDotString(chars, separator="   "):
  blocks = [charToDotString(char) for char in chars]
  lines = [block.splitlines() for block in blocks]
  lines = [separator.join(line) for line in zip(*lines)]
  return '\n'.join(lines)

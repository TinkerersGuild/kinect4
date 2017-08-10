import sys
import pytest
sys.path.append("../lib/")
import board as b


test_tiles = ([12,13], [11,37],[22,11], [13,24],  [13,48], [25,24])
print("Input: {}".format(test_tiles))
myboard = b.Board(4,4)
myboard.setTiles(test_tiles)

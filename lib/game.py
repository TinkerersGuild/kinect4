import sys
sys.path.append("../lib/")
import board as b


class Game:
    myboard = None

    def __init__(self, cols, rows):
        self.myboard = b.Board(cols, rows)
    def setTiles(self, tiles):
        #print(tiles)
        self.myboard.set_tiles(tiles)
    def getTiles(self):
        tiles = list()
        rows,cols, vals = self.myboard.list_tiles()
        for r in rows:
            for c in cols:
                tiles.append((c,r))
        return tiles
    def showBoard(self):
        bprint = ""
        rcount = 0
        rows, cols, vals =  self.myboard.list_tiles()
        for c in cols:
           bprint += "\t{}\t".format(c) 
        bprint += "\n"
        for row in rows:
            bprint += "{}".format(row) 
            for tile in vals[rcount]:
                bprint += "\t{}\t".format(tile.val)
            bprint += "\n" 
            rcount += 1
        
        return bprint
        

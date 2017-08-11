import numpy as np
import collections

class Tile:
    x = 0
    y = 0
    val = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def find_centre(self):
        return(self.x, self.y)
     

class Board:
    row_centres = list() 
    col_centres = list() 
    row_count = 0
    col_count = 0
    tiles = list()
    col_space = 25
    row_space = 25

    def __init__(self,  colcount, rowcount):
        #given a fairly complete list of tiles, we should be able to
        #fill in the blanks.
        self.col_count = colcount
        self.row_count = rowcount
    def list_tiles(self):
        return (self.row_centres, self.col_centres,self.tiles)

    def set_tiles(self, tiles):
        print("Found {} circles: ".format(len(tiles)))
        # We want to group by row, but there might be missing data. If
        # we get the first X, we should be able to see "gaps"
        
        cols = list()
        rows = list()
        rav = list()
        cav = list()
        for t in tiles:
            cols.append(int(t[0]))
            rows.append(int(t[1]))
        rows.sort()
        self.row_space = (rows[-1] - rows[0])/(self.row_count -1)
        
        cols.sort()
        self.col_space = (cols[-1] - cols[0])/(self.col_count -1)
        print(rows)
        print(cols)
        self.build_averages(rows, self.row_centres, self.row_space)
        self.build_averages(cols, self.col_centres, self.col_space)
        print(self.row_centres)
        print(self.col_centres)
        self.build_tiles()
            
    def build_tiles(self):
        for r in self.row_centres:
            row = list()
            for c in self.col_centres:
                row.append(Tile(c,r))
            self.tiles.append(row)

    def build_averages(self, source, dest, spacing):
        dest.append( source[0])
        index = 0
        for i in source:
            if abs(dest[index] - i) < spacing/2: 
                dest[index] = int((dest[index] + i) / 2)
            else:
                print("{}, {}".format(index, dest[index]))
                index += 1
                dest.append(i)


        
        

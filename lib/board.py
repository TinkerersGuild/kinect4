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
    col_space = 5
    row_space = 5

    def __init__(self,  colcount, rowcount):
        #given a fairly complete list of tiles, we should be able to
        #fill in the blanks.
        self.col_count = colcount
        self.row_count = rowcount
    def list_tiles(self):
        return (self.row_centres, self.col_centres,self.tiles)

    def set_tiles(self, tiles):
        # We sort into rows - should get the top row firsti
        sort_t = list(tiles)
        print(sort_t)
        c, r = zip(*list(tiles))
        # We want to group by row, but there might be missing data. If
        # we get the first X, we should be able to see "gaps"
        rows = list(r)
        cols = list(c)
        rows.sort()
        self.row_centres.append(rows[0])
        cols.sort()
        self.col_centres.append(cols[0])
        self.build_averages(rows,self.row_centres, self.row_space)
        self.build_averages(cols,self.col_centres, self.col_space)
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
        index = 0

        for val in source: 
            dupe = 0
            c = dest[index]
            if abs(val - c) < spacing:
                #print("Same column: {}, {} ".format(val, c)) 
                    # It's in the same row/column, average the value
                dupe = 1
                dest[index] = (c + val)//2 
            if (dupe == 0):
                #print("New column centre: {}".format(val))
                dest.append( val)
                index += 1

            
        
            

        
        

from z3 import *
print("from z3 import * #done!")
class SudokuConditions:
    """
    Sudoku - like puzzels need 'always' these info for z3-solvers
    1. ONE input: the size of the square: size x size (default is 3)
    z3 needs size**2 integer-variables called: A[i][j]  in in j in range(size)
    First condition: all values of a cell ar between a and size -1
    Second condition: rows and colums are all different
    Third: a way to fill in given cell-values, here: instance
    """
    def __init__(self, size=3, DBG=False):
        self.size = size
        if DBG:
            print('got: size = {}'.format(self.size))
        self.randen = ['u','r','d','l']
        self.instance = [[0 for i in range(self.size)] for j in range(self.size)]  
        self.A = [ [ Int("a_%s_%s" % (i, j)) for j in range(self.size) ]  \
                  for i in range(self.size) ] 
        #PKHG>OK print('SS L14 A = {}'.format(self.A))
        
        #elements are between 1 and size -1 
        self.cells_c  = [ And(1 <= self.A[i][j], self.A[i][j] <= self.size)
          for i in range(self.size) for j in range(self.size) ]   
        # each row contains a digit at most once
        self.rows_c   = [ Distinct(self.A[i]) for i in range(self.size) ]
        #A[i] all of row i
        self.cols_c   = [ Distinct([ self.A[i][j] for i in range(self.size)]) 
               for j in range(self.size)]
        #use insctance to set know values
        #print('*_c = {}'.format(self.rows_c))
        print('A, cells_c, rows_c, cols_c , instance NOW in SC available')
  
    

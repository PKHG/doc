def getFPnameDate(voor = "CALCUDOKU", showname = False):
    """
        for saving results in a file
    """
    from datetime  import datetime
    d0, d1  = str(datetime.now()).split(" ")
    result =  "./resultfiles/" + voor + (d0[5:] + "_" + d1[0:2] + d1[3:5]).replace("-","") + ".py"
    if showname:
        print(result)
    return result

#should have been done before importing this module ;-)

from z3 import * 

def calcudoku_function(size, data, maxaantal = 3, inbetweenResult = False):
    """
    solve an calcudoku
    #Assumed: from z3 import * 
    input the size n of an n x n square
    data the geometry of the puzzel
    """
    #maxaantal = 3 #means show ONE ##or moew solution if exists
    #Assumed: from z3 import * 
    #if needed as seperate module: from mydateFP import getFPnameDate

    #print inbetween results: call with extra parameter:
    #inbetweenResult = True
    r = []
    fpname = getFPnameDate("CALCUDOKU6x6") #My test was a 6x6 CalcuDoku
    if inbetweenResult:
        print("results will be saved in  (this working dir): ", fpname)

    fp = open(fpname , "w")

    #input!: size = 6

    instance =  [ [0 for i in range(size)]
                       for j in range(size)]

    # size x size  matrix of integer variables, zero based indexing!
    #because of typing problems x and X  A is used
    #create the variables for the square
    A = [ [ Int("a_%s_%s" % (i, j)) for j in range(size) ]
      for i in range(size) ]

    # each cell contains a value in {1, ..., size}
    cells_c  = [ And(1 <= A[i][j], A[i][j] <= size)
             for i in range(size) for j in range(size) ]
    # each row contains a digit at most once
    rows_c   = [ Distinct(A[i]) for i in range(size) ] #A[i] all of row i

    #PKHG>??? ??? meaningfull, superflous coditions????
    #sumofAll = sum([i for i in range(1, size + 1)])
    #PKHG>??? rowssum_c = [Sum(A[i]) == sumofAll for i in range(size)]

    # each column contains a digit at most once
    cols_c   = [ Distinct([ A[i][j] for i in range(size)]) 
               for j in range(size)]

    #Same question for the columsums
    #PKHG>??? colssum_c = [ A[0][i] + A[1][i] + A[2][i] + A[3][i] + A[4][i]  + A[5][i] == 21 for i in range(size)]
    
    #this has do be done ( ;-( ) by hand
    #EXAMPLE of data for a 6 x 6
    """
    data = allgivenInfo = [Or(And(A[0][4] > A[0][5], A[0][4] / A[0][5] == 4),
                   And(A[0][5] > A[0][4], A[0][5] / A[0][4] == 4)),
                Or(And(A[5][4] > A[5][5], A[5][4] - A[5][5] == 3),
                   And(A[5][5] > A[5][4], A[5][5] - A[5][4] == 3)),
                Or(And(A[3][1] > A[4][1], A[3][1] - A[4][1] == 3),
                   And(A[4][1] > A[3][1], A[4][1] - A[3][1] == 3)),
                Or(And(A[1][5] > A[2][5], A[1][5] / A[2][5] == 3), 
                   And(A[2][5] > A[1][5], A[2][5] / A[1][5] == 3)),
                Or(And(A[2][3] > A[2][4], A[2][3] / A[2][4] == 6),
                   And(A[2][4] > A[2][3], A[2][4] / A[2][3] == 6)),
                A[0][1] + A[0][2] + A[1][1] == 14,
                A[4][3] * A[4][4] * A[5][3] == 40,
                A[0][3] * A[1][2] * A[1][3]  * A[1][4] == 300,
                A[2][1] * A[2][2] * A[3][2] * A[4][2] == 120,                 
                A[3][3] + A[3][4] + A[3][5] + A[4][5] ==17,
                A[4][0] + A[5][0] + A[5][1] + A[5][2] == 11,
                A[3][3] + A[3][4] + A[3][5] + A[4][5] == 17,
                A[4][3] * A[4][4] * A[5][3]  == 40,
               ]
    """

    #all conditions put together
    
    #PKHG>??? calcudoku_c = cells_c + rows_c + cols_c  +  rowssum_c + colssum_c + allgivenInfo
    calcudoku_c = cells_c + rows_c + cols_c  + data


    # calcudoku  instance, we use '0' for empty cells
    instance_c = [ If(instance[i][j] == 0,
                  True,
                  A[i][j] == instance[i][j])
               for i in range(size) for j in range(size) ]

    allSolutions = []
    s = Solver()
    s.add(calcudoku_c + instance_c) 

    #while loop will stop if counter is >= maxaantal, or 
    #no new solutions anymore found
    counter  = 0
    
    while s.check() == sat:
        counter += 1
        fp.write("p" + str(counter) + " = ")
        m = s.model()
    
        #solution as one big int ;-)
        r = [ [ m.evaluate(A[i][j]) for j in range(size) ]
              for i in range(size) ]
        t = ""
        for el in r:
            #print(el)
            res = [ "" + str(c) for c in el]
            tmp = "".join(res)
            t += tmp
        fp.write(t + "\n")
    
        #save solutions
        ns = t  #t is build as str now a big integer
        allSolutions.append(ns)
    
        #print(len(allSolutions))
        #print(counter , t)
        if inbetweenResult:
            print_matrix(r)
    
        # the solution found will be not anymore allowed: Not(And(vals))
        # Help from Nikolaj for looking for more solutions ;-)
        
        vals = [A[i][j] == m.evaluate(A[i][j]) for j in range(size)
            for i in range(size)]
        s.add(Not(And(vals)))
        if counter > maxaantal:  #not infinite while!!!
            break
    fp.close() #close the result file (do not forget)
    allSolasSet = set(allSolutions)
    if inbetweenResult:
        if counter:
            print("all different?" , len(allSolutions) == counter, "counter = ", counter)
        else:
            print("no solution, check instance", instance)
                    
    return (counter, r)

def getFPnameDate(voor = "eightQueens", showname = False):
    from datetime  import datetime
    d0, d1  = str(datetime.now()).split(" ")
    #print (d0,d1)
    result =  "./resultfiles/" + voor + (d0[5:] + "_" + d1[0:2] + d1[3:5]).replace("-","") + ".py"
    if showname:
        print(result)
    return result
#getFPnameDate()

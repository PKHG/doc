def getFPnameDate(voor = "mixSodudoku"):
    from datetime  import datetime
    d0, d1  = str(datetime.now()).split(" ")
    print (d0,d1)
    return voor + (d0[5:] + "_" + d1[0:2] + d1[3:5]).replace("-","") + ".py"
getFPnameDate()

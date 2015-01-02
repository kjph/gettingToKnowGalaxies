#-------------------------------------------------------------------------------
#Open ssneddb1_flat.dat file and extract RA for given glxy
#Note ssneddb1_flat.dat file may be renamed, hence the use of
#the defintion argument 'database' in place of the filename
#The column index in 'parts[10]' is specified in the header of the
#database file
def glxy_get_RA(glxy, database):
    readIn=open(database, 'r')
    for line in readIn:
        #bypass headers in database file
        if (line[0]=='#'):
            pass
        else:
            parts=line.split('|')
            if (parts[0]==glxy):
                #Prevent program termination
                try:
                    return parts[10]
                except IndexError, err:
                    print err
                    return None
    readIn.close()

#-------------------------------------------------------------------------------
#Open ssneddb1_flat.dat file and extract DEC for given glxy
#Note ssneddb1_flat.dat file may be renamed, hence the use of
#the defintion argument 'database' in place of the filename
#The column index in 'parts[11]' is specified in the header of the
#database file
def glxy_get_DEC(glxy, database):
    readIn=open(database, 'r')
    for line in readIn:
        #bypass headers in database file
        if (line[0]=='#'):
            pass
        else:
            parts=line.split('|')
            if (parts[0]==glxy):
                #prevent program termination
                try:
                    return parts[11]
                except IndexError, err:
                    print err
                    return None
    readIn.close()

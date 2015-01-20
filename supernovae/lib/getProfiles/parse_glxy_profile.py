import os
import glob

FILE='tmp_testbrightness.profile'
TARGET='./tmp_testprofileget.txt'
DIR='../../data/opticalProfiles/'

def alphaNumPassFilter(string):
    loweredString=string.lower()
    return re.sub(r'\W+', '', loweredString)

def return_profilePath(galaxy):
    #Determine file path for associated profile to the specified galaxy
    filePath=os.path.abspath(os.path.join(DIR,galaxy))
    filePath=glob.glob('%s*' % filePath)

    #Determine which file of the many (if there are many) to use

    #return path for opening later in program
    return filePath

def return_galIndex(galaxy):
    #Galaxies with the ":s#" suffix are those with galindexs
    galaxy=galaxy.lower()
    src_string=":s"
    if src_string in galaxy:
        galIndex=galaxy[galaxy.find(src_string)+len(src_string)]
        return galIndex
    #Indicates that there are no galindexes
    else:
        return -1

def getParameters(inFile, outFile):
    readIn=open(inFile, 'r')
    writeOut=open(outFile, 'w')
    for line in readIn:
        if 'AXERAT' in line:
            writeValue=line.split()[3]
            writeString='AXERAT='+writeValue+'\n'
            writeOut.write(writeString)
        elif 'XCENTER' in line:
            writeValue=line.split()[3]
            writeString='XCENTER='+writeValue+'\n'
            writeOut.write(writeString)
        elif 'YCENTER' in line:
            writeValue=line.split()[3]
            writeString='YCENTER='+writeValue+'\n'
            writeOut.write(writeString)
        elif 'PA' in line:
            writeValue=line.split()[3]
            writeString='PA_IMAGE='+writeValue+'\n'
            writeOut.write(writeString)
        elif 'PIXSIZE' in line:
            writeValue=line.split()[3]
            writeString='PIXSIZE='+writeValue+'\n'
            writeOut.write(writeString)
        else:
            pass

    readIn.close()
    writeOut.close()



#Need to determine which of galax is the correct one to use in the profie (as
#one profile may descrie multiple profiles (delimited by GALINDEX)

if __name__=='__main__':
    #getParameters(FILE, TARGET)
    #getProfile('J0209-10')
    print return_galIndex("J0209-10:S5")



import os
import glob

FILE='tmp_testbrightness.profile'
TARGET='./tmp_testprofileget.txt'
DIR='../../data/opticalProfiles/'

def alphaNumPassFilter(string):
    loweredString=string.lower()
    return re.sub(r'\W+', '', loweredString)

def return_profilePath(galaxy):
    galaxy=galaxy.lower()
    #Determine file path for associated profile to the specified galaxy

    #Get rid of galIndex identifier for filename
    identifier=":s"
    if identifier in galaxy:
        galaxy=galaxy[:galaxy.find(identifier)]
        galaxy=galaxy.upper()

    filePath=os.path.abspath(os.path.join(DIR,galaxy))
    filePath=glob.glob('%s*' % filePath)

    #Determine which file of the many (if there are many) to use

    #return path for opening later in program
    return filePath

def return_galIndex(galaxy):
    #Galaxies with the ":s#" suffix are those with galindexs
    galaxy=galaxy.lower()
    #is ":s" a unique identifier
    identifier=":s"
    if identifier in galaxy:
        galIndex=galaxy[galaxy.find(identifier)+len(identifier)]
        return int(galIndex)
    #Indicates that there are no galindexes
    else:
        return -1

def getParameters(galaxy, outFile):
    pixSize=0
    galIndex=return_galIndex(galaxy)
    try:
        readIn=open(return_profilePath(galaxy), 'r')
    except TypeError:
        readIn=open(return_profilePath(galaxy)[0], 'r')

    #Move cursor to start of extract
    if (galIndex != -1):
        for line in readIn:
            #Get common parameter PIXSIZE
            if 'PIXSIZE' in line:
                pixSize=line.split()[3]
            elif ('GALINDEX' in line):
                lineParts=line.split()
                if (int(lineParts[3]) == galIndex):
                    break

    writeOut=open(outFile, 'w')
    #read extract
    for line in readIn:
        print line#DEBUG
        #stop reading if end of extract
        if ('GALINDEX' in line and galIndex != -1):
            break
        elif 'AXERAT' in line:
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
        elif ('PA ' in line):
            writeValue=line.split()[3]
            writeString='PA='+writeValue+'\n'
            writeOut.write(writeString)
        else:
            pass

    #write common parameter PIXSIZE
    writeString='PIXSIZE=%s\n'%pixSize
    writeOut.write(writeString)

    readIn.close()
    writeOut.close()

#Need to determine which of galax is the correct one to use in the profie (as
#one profile may descrie multiple profiles (delimited by GALINDEX)

if __name__=='__main__':
    getParameters('J0209-10:S2', 'test.txt')

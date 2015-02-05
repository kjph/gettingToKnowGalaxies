FILE='tmp_testbrightness.profile'
TARGET='./tmp_testprofileget.txt'

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
        elif 'PA_IMAGE' in line:
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

if __name__=='__main__':
    getParameters(FILE, TARGET)


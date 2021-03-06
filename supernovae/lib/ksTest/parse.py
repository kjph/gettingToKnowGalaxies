#TEMP (as of 05/02/2015)
#This script will be used to collate all the necessary data into one TXT file
#This TXT file will be used in the KS-Test

#note about debugging
#All lines that are used for the purpose of debugging are prepended with the tag
#'#DEBUG'. However there are lines that are modified for debugging and cannot be
#removed completely from the program. These are prepended with the tag '#D2EBUG'

import re
import os
import glob
import ksTest_transform

#-------------------------------------------------------------------------------
#DEFINE PATHS
DATA_DIR="/Users/21326604/Downloads/gettingToKnowGalaxies/supernovae/data"
#DATA_DIR="/home/kph/Dropbox/files/gettingToKnowGalaxies/supernovae/data"
#DATA_DIR="/home/uniwa/students4/students/21326604/linux/Downloads/gettingToKnowGalaxies/supernovae/data"
MATCH_FILE=os.path.join(DATA_DIR,"out_supernovae_match_typeII.txt")
GLXY_DATA=os.path.join(DATA_DIR,"glxy_data.dat")
SN_DATA=os.path.join(DATA_DIR,"out_supernovae_get_pos.txt")
PROFILE_DIR=os.path.join(DATA_DIR,"opticalProfiles/")

#-------------------------------------------------------------------------------
def printDebug(glxy, iD, msg):
    print "[%s:%s]: %s" % (glxy, iD, msg)

#-------------------------------------------------------------------------------
#string is returned with only alphanumeric characters and lowercase
def alphaNumPassFilter(string):
    loweredString=string.lower()
    return re.sub(r'\W+', '', loweredString)

#-------------------------------------------------------------------------------
#Open ssneddb1_flat.dat file and extract RA for given glxy
#Note ssneddb1_flat.dat file may be renamed, hence the use of
#the defintion argument 'database' in place of the filename
#The column index in 'parts[10]' is specified in the header of the
#database file
def glxy_get_RA(glxy, database):
    glxy=alphaNumPassFilter(glxy)
    readIn=open(database, 'r')

    for line in readIn:
        #bypass headers in database file
        if (line[0]=='#'):
            pass
        else:
            parts=line.split('|')
            glxyRead_NNAME=alphaNumPassFilter(parts[1])#NEDNAME
            glxyRead_SNAME=alphaNumPassFilter(parts[0])#SNAME
            if (glxyRead_NNAME==glxy or glxyRead_SNAME==glxy):
                #Prevent program termination
                try:
                    return float(parts[10])
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
    glxy=alphaNumPassFilter(glxy)
    readIn=open(database, 'r')
    for line in readIn:
        #bypass headers in database file
        if (line[0]=='#'):
            pass
        else:
            parts=line.split('|')
            glxyRead_NNAME=alphaNumPassFilter(parts[1])#NEDNAME
            glxyRead_SNAME=alphaNumPassFilter(parts[0])#SNAME
            if (glxyRead_NNAME==glxy or glxyRead_SNAME==glxy):
                #prevent program termination
                try:
                    return float(parts[11])
                except IndexError, err:
                    print err
                    return None
    readIn.close()

#-------------------------------------------------------------------------------
#Profile related parsing
#Determine which profile is the approripate profile
#This function returns the path to this profile
def return_profilePath(galaxy):
    galaxy=galaxy.lower()
    #Determine file path for associated profile to the specified galaxy

    #Get rid of galIndex identifier for filename
    identifier=":s"
    if identifier in galaxy:
        galaxy=galaxy[:galaxy.find(identifier)]
        print "[%s:96] Searching profile for %s" % (galaxy,galaxy)#DEBUG
        galaxy=galaxy.upper()

    filePath=os.path.abspath(os.path.join(PROFILE_DIR,galaxy))
    filePath=glob.glob('%s*' % filePath)

    #Determine which file of the many (if there are many) to use
    #FIX
    print "[%s], %s" % (galaxy,filePath)#DEBUG
    #if type(filePath) is list & len(filePath)>0:
    #    return filePath[0]
    #elif type(filePath) is str:
    #    return filePath
    #else:
    #    return -1

    return filePath

#-------------------------------------------------------------------------------
#Determine which galaxy index is the appropriate index that matches with the
#Concerned SN. Return -1 if no galaxy index is appropriate or required
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

#-------------------------------------------------------------------------------
#Get the profile parameters of the host galaxy and return as a tuple
def getParameters(galaxy):
    pixSize=0
    galIndex=return_galIndex(galaxy)
    try:
        readIn=open(return_profilePath(galaxy), 'r')
    except TypeError,err:
        print "[%s:137]: %s" % (galaxy,err)#DEBUG
        try:
            readIn=open(return_profilePath(galaxy)[0], 'r')
        except IndexError:
            print "[%s:141]: %s: No profile found" % (galaxy,galaxy)#DEBUG
            return -1 #Indicates no profile was found

    #Intialization
    printDebug(galaxy,"149","initialized done")
    (pp_pixSize, pp_axeRat, pp_xCenter, pp_yCenter, pp_pa)=(-1,-1,-1,-1,-1)

    #Move cursor to start of extract
    printDebug(galaxy,"153",galIndex)
    if (galIndex != -1):
        for line in readIn:
            #Get common parameter PIXSIZE
            if 'PIXSIZE' in line:
                pp_pixSize=line.split()[3]
            #Move cursor to correct position
            elif ('GALINDEX' in line):
                lineParts=line.split()
                if (int(lineParts[3]) == galIndex):
                    break

    #read extract
    for line in readIn:
        #stop reading if end of extract
        if (('GALINDEX' in line) and (galIndex != -1)):
            break
        elif 'PIXSIZE' in line:
            pp_pixSize=line.split()[3]
            printDebug(galaxy,"169",pp_pixSize)
        elif 'AXERAT' in line:
            pp_axeRat=line.split()[3]
            printDebug(galaxy,"175",pp_axeRat)
        elif 'XCENTER' in line:
            pp_xCenter=line.split()[3]
        elif 'YCENTER' in line:
            pp_yCenter=line.split()[3]
        elif ('PA ' in line):
            pp_pa=line.split()[3]
        else:
            pass

    readIn.close()
    return (pp_pixSize, pp_axeRat, pp_xCenter, pp_yCenter, pp_pa)
#-------------------------------------------------------------------------------
#Need to extract SN coord's
def get_SN_coords(SN, database):
    readIn=open(database,'r')

    sNova=alphaNumPassFilter(SN)

    for line in readIn:
        if (line[0]=='#'):
            pass
        else:
            parts=line.split(',')
            SN_readName=alphaNumPassFilter(parts[0])#NEDNAME
            if (SN_readName==sNova):
                #Prevent program termination
                try:
                    return (float(parts[1]),float(parts[2]))
                except IndexError, err:
                    print err
                    return None
    readIn.close()

#-------------------------------------------------------------------------------
#Formats the text file output
#Formatted file will have these columns
#Host   HOST(RA,DEC)   SN   SN(RA,DEC)    Profile Parameters --->
def format_output(outputFile):
    write_out=open(outputFile, 'w')
    read_in=open(MATCH_FILE, 'r')

    #Write Header
    headerString="%s%10s%20s%10s%20s%20s%10s%10s%10s%10s%10s\n" % ("{0: <20}".format("HOST"), "HOST-RA", "HOST-DEC", "SN", "SN-RA", "SN-DEC", "PIX-SIZE", "AXE-RAT", "X-CENTER", "Y-CENTER", "PA")
    write_out.write(headerString)

    for line in read_in:
        parts=line.split(',')

        #GET SN COORD's
        sn=parts[1]
        try:
            (sn_ra,sn_dec)=get_SN_coords(sn, SN_DATA)
        except TypeError:
            (sn_ra,sn_dec)=(-1,-1)

        #GET GALAXY-RELATED PARAMETERS
        glxy=parts[0]
        glxy_ra=glxy_get_RA(glxy, GLXY_DATA)
        glxy_dec=glxy_get_DEC(glxy, GLXY_DATA)
        try:
            (pp_pixSize, pp_axeRat, pp_xCenter, pp_yCenter, pp_pa)=getParameters(glxy)
            vec_GX_SN=ksTest_transform.get_vec_GX_SN(sn_ra, sn_dec, glxy_ra, glxy_dec)
            print "[%s:230]: %s" % (glxy,vec_GX_SN)#DEBUG
            semiMajorLength=ksTest_transform.get_A(pp_pixSize, pp_axeRat, pp_pa, vec_GX_SN)
            printDebug(glxy, "240", "passed")
        except TypeError,err:#D2EBUG
            print "[%s]: 226: %s " % (glxy, str(err))#DEBUG
            (pp_pixSize, pp_axeRat, pp_xCenter, pp_yCenter, pp_pa, semiMajorLength)=(-1,-1,-1,-1,-1,-1)

        #MERGE TO ONE STRING
        writeString="%s%10s%20s%10s%20s%20s%10s%10s%10s%10s%10s%20s\n" % ('{0: <20}'.format(glxy), glxy_ra, glxy_dec, sn, sn_ra, sn_dec, pp_pixSize, pp_axeRat, pp_xCenter, pp_yCenter, pp_pa, semiMajorLength)

        write_out.write(writeString)

    write_out.close()
    read_in.close()

format_output("test.txt")

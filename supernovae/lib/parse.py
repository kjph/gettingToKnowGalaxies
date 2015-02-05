#TEMP (as of 05/02/2015)
#This script will be used to collate all the necessary data into one TXT file
#This TXT file will be used in the KS-Test

import re
import os
import glob

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
        galaxy=galaxy.upper()

    filePath=os.path.abspath(os.path.join(DIR,galaxy))
    filePath=glob.glob('%s*' % filePath)

    #Determine which file of the many (if there are many) to use

    #return path for opening later in program
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
                pp_pixSize=line.split()[3]
            #Move cursor to correct position
            elif ('GALINDEX' in line):
                lineParts=line.split()
                if (int(lineParts[3]) == galIndex):
                    break

    #read extract
    for line in readIn:
        #stop reading if end of extract
        if ('GALINDEX' in line and galIndex != -1):
            break
        elif 'PIXSIZE' in line:
            pp_pixSize=line.split()[3]
        elif 'AXERAT' in line:
            pp_axeRat=line.split()[3]
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

#-------------------------------------------------------------------------------
#Formats the text file output
#Formatted file will have these columns
#Host   HOST(RA,DEC)   SN   SN(RA,DEC)    Profile Parameters --->
def format_output(outputFile):
    write_out=open(outputFile, 'w')

    #WRITE HEADER

    #for line in #MATCHFILE:
	    #galaxy=line[#IDENTIFIER]
	    #matched_sn=line[#IDENTIFER]
	    #glxy_get_RA(glxy, #DATABASE)
        	#glxy_get_DEC(glxy, #DATABASE)
	    #get_profile_parameters(....)
	    ##GET SN COORD's
	    #	....
	    #	....
	    #
	    ##MERGE TO ONE STRING
	    #writeString="%s\t%s\t%s\t%s\n" % (glxy, ...)
	    #write_out.write(writeString)

    write_out.close()

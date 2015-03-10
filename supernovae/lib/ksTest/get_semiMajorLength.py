#A module to determine the semi-major axis length of the ellipse that passes
#through the SN and who's axis are parallel to its host galaxy
import numpy
import sys
import math

def die(message):
    PROG=sys.argv[0]
    print("%s: %s" % PROG, message)
    quit()

#Returns the supernovae offset from the center of its host galaxy in RA an DEC
#degrees as a numpy object
def get_vec_GX_SN(SN_RA, SN_DEC, GX_RA, GX_DEC):
    return numpy.array([SN_RA-GX_RA, SN_DEC-GX_DEC])

#Returns the semi major axis length of the ellipse passing through the SN and is
#parallel to the semi-major/minor axis of its host galaxy
def get_A(PIXRAT, AXERAT, POSANGLE, vec_GX_SN):
    if type(vec_GX_SN).__module__ != 'numpy':
        die("vec_GX_SN must be a numpy type array")
        return NULL

    XY_transform = numpy.array([1/(3600*PIXRAT), 1/(3600*PIXRAT)])
    vec_GX_SN = XY_transform*vec_GX_SN
    AB_transform_return_A = numpy.array([AXERAT*math.sin(POSANGLE), AXERAT*math.cos(POSANGLE)])
    return numpy.dot(AB_transform_return_A, vec_GX_SN)
	
#Opens the output file of the getParameters function in the Parse_glxy_profile
#module and uses get_A to append the output file with the Semi-Major Axis Length
def getPars(filename, vec_GX_SN):
	file = open(filename, 'a+')
	for line in file:
		if 'XCENTER' in line:
			xCenter = line.split('=')[1]
		elif 'YCENTER' in line:
			yCenter = line.split('=')[1]
		elif 'AXERAT' in line:
			axeRat = line.split('=')[1]
		elif 'PA' in line:
			pA = line.split('=')[1]
		elif 'PIXSIZE' in line:
			pixSize = line.split('=')[1]
		else:
			pass
	
	a = get_A(pixSize, axeRat, pA, vec_GX_SN)
	toWrite = "AXISLENGTH=%d" % a
	file.write(toWrite)
	file.close()
	return None
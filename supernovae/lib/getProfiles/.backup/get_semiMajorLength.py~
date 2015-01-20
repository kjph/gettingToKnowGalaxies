#A module to determine the semi-major axis length of the ellipce that passes
#through the SN and whos axis are parallel to its host galaxy
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

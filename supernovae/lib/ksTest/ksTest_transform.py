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

    PIXRAT=float(PIXRAT)
    AXERAT=float(AXERAT)
    POSANGLE=float(POSANGLE)
    XY_transform = numpy.array([3600/PIXRAT, 3600/PIXRAT])#changed from 1/(3600*PIXRAT) (Alex)
    vec_GX_SN = XY_transform*vec_GX_SN
    AB_transform_return_A = numpy.array([AXERAT*math.sin((POSANGLE*math.pi)/180), AXERAT*math.cos((POSANGLE*math.pi)/180)])#changed angle to radians (Alex)
    semiMajorA=numpy.dot(AB_transform_return_A, vec_GX_SN)
    return semiMajorA


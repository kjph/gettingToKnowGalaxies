[1mdiff --git a/supernovae/lib/getProfiles/get_semiMajorLength.py b/supernovae/lib/getProfiles/get_semiMajorLength.py[m
[1mindex ed5799e..6859a72 100644[m
[1m--- a/supernovae/lib/getProfiles/get_semiMajorLength.py[m
[1m+++ b/supernovae/lib/getProfiles/get_semiMajorLength.py[m
[36m@@ -1,5 +1,5 @@[m
[31m-#A module to determine the semi-major axis length of the ellipce that passes[m
[31m-#through the SN and whos axis are parallel to its host galaxy[m
[32m+[m[32m#A module to determine the semi-major axis length of the ellipse that passes[m
[32m+[m[32m#through the SN and who's axis are parallel to its host galaxy[m
 import numpy[m
 import sys[m
 import math[m
[36m@@ -25,3 +25,27 @@[m [mdef get_A(PIXRAT, AXERAT, POSANGLE, vec_GX_SN):[m
     vec_GX_SN = XY_transform*vec_GX_SN[m
     AB_transform_return_A = numpy.array([AXERAT*math.sin(POSANGLE), AXERAT*math.cos(POSANGLE)])[m
     return numpy.dot(AB_transform_return_A, vec_GX_SN)[m
[32m+[m[41m	[m
[32m+[m[32m#Opens the output file of the getParameters function in the Parse_glxy_profile[m
[32m+[m[32m#module and uses get_A to append the output file with the Semi-Major Axis Length[m
[32m+[m[32mdef getPars(filename, vec_GX_SN):[m
[32m+[m	[32mfile = open(filename, 'a+')[m
[32m+[m	[32mfor line in file:[m
[32m+[m		[32mif 'XCENTER' in line:[m
[32m+[m			[32mxCenter = line.split('=')[1][m
[32m+[m		[32melif 'YCENTER' in line:[m
[32m+[m			[32myCenter = line.split('=')[1][m
[32m+[m		[32melif 'AXERAT' in line:[m
[32m+[m			[32maxeRat = line.split('=')[1][m
[32m+[m		[32melif 'PA' in line:[m
[32m+[m			[32mpA = line.split('=')[1][m
[32m+[m		[32melif 'PIXSIZE' in line:[m
[32m+[m			[32mpixSize = line.split('=')[1][m
[32m+[m		[32melse:[m
[32m+[m			[32mpass[m
[32m+[m[41m	[m
[32m+[m	[32ma = get_A(pixSize, axeRat, pA, vec_GX_SN)[m
[32m+[m	[32mtoWrite = "AXISLENGTH=%d" % a[m
[32m+[m	[32mfile.write(toWrite)[m
[32m+[m	[32mfile.close()[m
[32m+[m	[32mreturn None[m
\ No newline at end of file[m

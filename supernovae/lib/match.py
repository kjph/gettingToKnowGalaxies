#To match two catalgoues together by closest separation distance
#This has to be configured manually

import csv
import numpy
import sys
from astropy.coordinates import SkyCoord
from astropy.coordinates import angles
from astropy import units

def load_cat(filename,delim,nameIndex,raIndex,decIndex):
	catObjNames=[]
	catObjRADeg=[]
	catObjDecDeg=[]
	with open(filename, 'rb') as target:
		for row in target:
			if delim==' ':
				cat=row.split()
			else:
				cat=row.split(delim)
			catObjNames.append(cat[nameIndex])
			catObjRADeg.append(float(cat[raIndex]))
			catObjDecDeg.append(float(cat[decIndex]))

		return numpy.array(catObjNames), numpy.array(catObjRADeg), numpy.array(catObjDecDeg)

def write_results(output_file, index, dist2D, cat1_name, cat2_name):
	csvFile=open(output_file, 'w')
        repeatCheck = {}

	for i,j in enumerate(index):
            tolerance_deg = 8.0/60.0
            separation = float(dist2D[i].to_string(decimal=True))
            if separation < tolerance_deg:
                try:
                    if separation > repeatCheck['%s' % cat1_name[i]]:
                        repeatCheck['%s' % cat1_name[i]] = (float(dist2D[i].to_string(decimal=True)),j) #store as tuple
                    else:
                        pass
                except KeyError:
                        repeatCheck['%s' % cat1_name[i]] = (float(dist2D[i].to_string(decimal=True)),j) #store as tuple

        for cat1, value in repeatCheck.iteritems():
            CSVString=cat1+','+cat2_name[value[1]]+','+'%f' % value[0]+'\n'
            csvFile.write(CSVString)
        csvFile.close()

def main(output_file):
	cat1_name, cat1_RADeg, cat1_DecDeg=load_cat('../data/g_singg_galaxyinfo_noheaders','|',0,10,11)
	cat2_name, cat2_RADeg, cat2_DecDeg=load_cat('../data/out_iau_supernovae_get_pos.txt',',',0,1,2)
	cat1=SkyCoord(ra=cat1_RADeg*units.degree, dec=cat1_DecDeg*units.degree)
	cat2=SkyCoord(ra=cat2_RADeg*units.degree, dec=cat2_DecDeg*units.degree)
	index,dist2D,dist3D=cat1.match_to_catalog_sky(cat2)
	write_results(output_file, index, dist2D, cat1_name, cat2_name)

main()

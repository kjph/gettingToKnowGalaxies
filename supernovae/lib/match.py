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

def remove_repeats(output_file):
    #Open file for reading and save lines to list
    #Close file immediately; parse from list
    #This ensures that the file can be overwritten without
    #The need for a buffer
    target=open(output_file, 'r')
    lines=target.readlines()
    target.close()

    #make SN the first element in the list
    lines=[x.split(',') for x in lines]
    lines=lines[1:]#Get rid of header
    lines=[[x[1],x[3],x[0]] for x in lines]#Having distances as second column
    lines=[','.join(x) for x in lines]

    #sort alphabetically
    lines.sort()#The closest match will be the first for each SN occurance


    #Remove all subsequent occurances of repeated SN, as the first one is the
    #closest match
    prevSN=lines[0].split()[0]
    for line in lines[1:]:
        SN=line.split()[0]
        if (SN == prevSN):
            lines.remove(line)
        else:
            prevSN=SN

    #Re order list
    lines=[x.split(',') for x in lines]
    lines=[[x[2],x[0],x[1]] for x in lines]
    lines=[','.join(x) for x in lines]

    #write to target
    writeString=''.join(lines)
    target=open(output_file,'w')
    target.write(writeString)
    target.close()

def main(output_file):
	#cat1_name, cat1_RADeg, cat1_DecDeg=load_cat('../data/g_singg_galaxyinfo_noheaders','|',0,10,11)
	#cat2_name, cat2_RADeg, cat2_DecDeg=load_cat('../data/out_iau_supernovae_get_pos.txt',',',0,1,2)
	#cat1=SkyCoord(ra=cat1_RADeg*units.degree, dec=cat1_DecDeg*units.degree)
	#cat2=SkyCoord(ra=cat2_RADeg*units.degree, dec=cat2_DecDeg*units.degree)
	#index,dist2D,dist3D=cat1.match_to_catalog_sky(cat2)
	#write_results(output_file, index, dist2D, cat1_name, cat2_name)
    remove_repeats(output_file)

main('../data/test_match.txt')

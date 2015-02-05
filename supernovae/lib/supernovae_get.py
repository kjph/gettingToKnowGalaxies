#===============================================================================
# Supernovae data collection
#===============================================================================
#
# Author:       Khanh J. Phan
# Email:        21326604@student.uwa.edu.au
#               jme.ph2@gmail.com
# Last updated: 16/12/2014
#
#===============================================================================

import requests
import itertools
import os
import sys
import re
import time
import subprocess
import glob
#import match            #match.py from working directory
from astropy import units as u
from astropy.coordinates import SkyCoord

#=== TOOLS =====================================================================
#Simple logging function
def print_status(out_string):
    OUTPROMPT = '[' + time.strftime('%X') + (' %s' % sys.argv[0]) + ']'
    print("%s: %s" % (OUTPROMPT,out_string))

#To manage buffers and temporary streams
#Fetched data is stored into a buffer
#This function then transfers the data in that buffer
#to the desired location.
def commit_temp(save_file_loc):
    save_file_loc_temp = save_file_loc + '.temp'
    target=open(save_file_loc, "w")
    temp=open(save_file_loc_temp, "r")

    for line in temp:
        target.write(line)

    target.close()
    temp.close()
    os.remove(save_file_loc_temp)

def RAToDeg(hours,mins,secs):
    return (hours*15.0 + (15.0/60.0)*mins + (15.0/3600.0)*secs)

def DECToDeg(sign,degs,arcm,arcs):
    if sign=='+':
        return (degs + (1.0/60.0)*arcm + (1.0/3600.0)*arcs)
    if sign=='-':
        return ((-1.0)*(degs + (1.0/60.0)*arcm + (1.0/3600.0)*arcs))

#=== FETCH =====================================================================
#Download the IAU supernovae table source code.
#File is saved into OUT_DIR/SN_DB_FILE
#See global variables @ bottom of file
def get_source():
    """Get HTML source from IAU website and save into specified dir."""
    print_status("Downloading source code file")

    resp=requests.get(IAU_URL, stream=True)

    #No need for buffer as it is first time opening file
    output=open(SN_DB_FILE, "w")

    output.write(resp.raw.read())
    output.close()

#Removes HTML headers from IAU fetched data
#The HTML headers terminate at the unique tag <pre>
#This may need updating if the IAU page updates
def removeHeader_source():
    print_status("Removing header from source code file")

    target=open(SN_DB_FILE, "r")
    temp=open(SN_TMP_FILE, "w")

    i = 0
    write_status = 0
    for line in target:
        if write_status == 1:
            temp.write(line)
        else:
            i = i+1
        if line.strip() == '<pre>':
            write_status = 1
        else:
            pass

    target.close()
    temp.close()
    commit_temp(SN_DB_FILE)

#Removes HTML footers from IAU fetched data
#The HTML footers begin at the unique tag </pre>
#This may need updating if the IAU page updates
def removeFoot_trim_source():
    """Remove footers from saved source file."""
    print_status("Removing foot from source and trimming file")

    lines=open(SN_DB_FILE, "r").readlines()

    for i, line in enumerate(lines):
        if line.strip()=="":
            del lines[i]
        elif line.strip()=="</pre>":
            last = i
        else:
            pass

    open(SN_TMP_FILE, "w").writelines(lines[1:last])
    commit_temp(SN_DB_FILE)

#Removes remaining HTML tags wihtin fetched data
def clean_source():
    """Remove HTML tags from saved source file."""
    print_status("Cleaning source code file")

    target=open(SN_DB_FILE, "r")
    temp=open(SN_TMP_FILE, "w")

    for line in target:
        line_parts = line.split("</a>")

        #Because regex in Python is terrible and searches for longest possible
        #string when using wildcards with matching tags
        for i in range(len(line_parts)):
            line_parts[i] = re.sub(r'<a name=".*">', '', line_parts[i])
            line_parts[i] = re.sub(r'<a href="?\'?([^"\'>]*)">', '', line_parts[i])
            line_parts[i] = re.sub(r'<i>', '', line_parts[i])
            line_parts[i] = re.sub(r'</i>', '', line_parts[i])
        line = ''.join(line_parts)
        temp.write(line)

    target.close()
    temp.close()
    commit_temp(SN_DB_FILE)

#Write custom header into fetched data
def write_header():
    """Write header to output and save as text file."""
    print_status("Writing header to output file")

    target=open(SN_DB_FILE, "r")
    temp=open(SN_TMP_FILE, "w")

    HEADER = "SN      Host Galaxy      Date        R.A.    Decl.    Offset Mag.  Disc. Ref.      SN Position               Posn. Ref.       Type  SN Discoverer(s)\n"
    temp.write(HEADER)

    for line in target:
        temp.write(line)

    target.close()
    temp.close()
    commit_temp(SN_DB_FILE)

#=== PARSE =====================================================================
def extract_sn_data():
    print_status("Selecting data and writing to new output")

    target=open(SN_DB_FILE, "r")
    output=open(SN_POS_FILE, "w")

    for row in target:
        sn_name             =row[0:8].strip()       #SN Name
        sn_ra               =row[87:98].strip()     #SN RA coord
        sn_dec              =row[99:110].strip()    #SN DEC coord
        sn_type             =row[130:136].strip()   #SN type
        #row[8:25].strip()     #Host galaxy
        #row[25:37].strip()    #Date
        #row[37:45].strip()    #RA of host galaxy
        #row[45:51].strip()    #DEC of host galaxy
        #row[51:57].strip()    #Offset east/west
        #row[57:62].strip()    #Offset north/south
        #row[62:68].strip()    #Mag
        #row[71:87].strip()    #Disc Ref
        #row[87:110].strip()   #Post

    #Select galaxies to include here
    if (sn_name=='' or sn_ra=='' or sn_dec==''):
        pass
    #elif (sn_type=='' or "?" in sn_type):
    #    #Flag for review
    #    pass
    #elif ("II" not in sn_type):
    #    pass
    else:
        sn_ra_deg = RAToDeg(float(sn_ra[0:2]), float(sn_ra[3:5]), float(sn_ra[6:11]))
        sn_dec_deg = DECToDeg(sn_dec[0],float(sn_dec[1:3]), float(sn_dec[4:6]), float(sn_dec[7:11]))
        out_string = "%s,%s,%s\n" % (sn_name, sn_ra_deg, sn_dec_deg)
        output.write(out_string)

    target.close()
    output.close()

#=== OUTPUT ====================================================================
#Generate a DS9 region file for each galaxy
#Containing supernovae
def regions_files():
    print_status("Generating DS9 Regions Files")

    pos_file    = open(SN_POS_FILE, "r")
    match_file  = open(MATCH_FILE, "r")

    sn_name, sn_ra_deg, sn_dec_deg = [],[],[]
    for row in pos_file:
        parts = row.split(',')
        sn_name.append(parts[0])
        sn_ra_deg.append(parts[1])
        sn_dec_deg.append(parts[2])

    pos_file.close()

    singg_name, match_index, sep, = [],[],[]
    for row in match_file:
        parts = row.split(',')
        singg_name.append(parts[0])
        match_index.append(sn_name.index(parts[1]))
        sep.append(parts[2])

    match_file.close()

    for i in range(len(singg_name)):
        filename = '%s/%s_regionfile.reg' % (OVERLAY_DIR,singg_name[i])
        if (os.path.isfile(filename) == True):
            regionfile = open(filename, "a")
        else:
            regionfile = open(filename, "w")
            headerstring = 'global color=green font="helvetica 20 normal roman" wcs=wcs\n'
            regionfile.write(headerstring)

        mainstring = 'j2000; circle %fd %fd %fd # text = {%s}\n' % (
            float(sn_ra_deg[match_index[i]]),
            float(sn_dec_deg[match_index[i]]),
            OVERLAY_RADIUS,
            sn_name[match_index[i]]
        )
        regionfile.write(mainstring)

    regionfile.close()

#input: g_datalist = listing of paths for relevant FITS images (from Google Drive)
#       match_file = match output found in DIR (not integrated to work with the
#       module yet...)
#

#Locates all the fits images relevant to each galaxy found in MATCH_FILE to a
#stfp compatible command file - STFP_FILE. The paths of all the galaxies can be
#found in the STFP_IMG_PATH_FILE. The STFP command file, when run through a
#terminal will download the specified fits images to the directory specifiec in
#the variable IMG_DIR
def get_fits_images():
    #Open files for reading
    dlist = open(STFP_IMG_PATH_FILE, "r").readlines()
    mfile = open(MATCH_FILE, "r")

    #Determine SINGG galaxies that had Supernovae matched and append to array
    singg_need = []
    for line in mfile:
        singg_need.append(line.split(',')[0])

    mfile.close()

    #Determine which of the SINGG galaxies in singg_need have FITS images
    #Save indicies to array
    lines_to_write = []
    for i,j in enumerate(dlist):
        singg = j.split()[0]
        if singg in singg_need:
            lines_to_write.append(i)

    #Using the indicies from above, write to a sftp output file
    sftp_file = open(SFTP_FILE, "w")
    for i in lines_to_write:
        dlist_parts = dlist[i].split()
        for i in [6,7,8]:
            remote_path = os.path.join(dlist_parts[5] + dlist_parts[i])
            filename_parts = os.path.splitext(dlist_parts[i])
            filename = filename_parts[0]
            exten = filename_parts[1]
            run = dlist_parts[1]
            new_filename = filename + '_' + run + exten
            local_path = os.path.join(IMG_DIR, new_filename)
            write_string = 'get %s %s\n' % (remote_path, local_path)
            sftp_file.write(write_string)
    sftp_file.close()

#Loop all images retrieved in IMG_DIR and overlay them with regions files
#This requires the overlay shell script to be in the same workign directory
#as the script
def loop_fits_images():
    fileList = [ f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR,f))]
    while(len(fileList)!=0):
            fileName = fileList[0]
            fileParts = fileName.split('_')
            galaxy = fileParts[0]
            run = re.sub('.fits', '', fileParts[len(fileParts)-1])
            print_status("attempting to overlay %s for %s" % (galaxy, run))
            subprocess.check_call([OVERLAY_SCRIPT, str(IMG_DIR), str(OVERLAY_DIR), str(galaxy), str(run)])
            glob_string = os.path.join(IMG_DIR, "%s*%s.fits" % (galaxy, run))
            exclude = [os.path.split(f)[1] for f in glob.glob(glob_string)]
            fileList = [f for f in fileList if f not in exclude]

#-------------------------------------------------------------------------------
# USER CONFIGURATIONS
#-------------------------------------------------------------------------------
def main():
    #--------------------------------------------------
    # Fetch the data from IAU
    #--------------------------------------------------
    get_source()
    removeHeader_source()
    removeFoot_trim_source()
    clean_source()

    #--------------------------------------------------
    # Parse the desired information from fetched data
    #--------------------------------------------------
    extract_sn_data()
    write_header()

    #--------------------------------------------------
    # Output
    #--------------------------------------------------
    #print_status("Matching supernovae to SINGG/SUNGG Galaxies")
    #match.main(MATCH_FILE)
    #regions_files()
    #get_fits_images()
    #loop_fits_images()

# SETTINGS
#IAU_URL                 : Specifies the URL to the IAU website which lists all recorded SN
#OUT_DIR                 : The directory where all outputs are directed (exc. FITS images. See IMG_DIR)
#SN_DB_FILE              : The name of the text file which contains the fetched SN listing. The absolute path of this file will be OUT_DIR/SN_DB_FILE
#SN_TMP_FILE             : A Temporary buffer to write into.
#SN_POS_FILE             : Similar to the SN_DB_FILE except the data is reduced, in a manner specified by the function def extract_sn_data()
#MATCH_FILE              : Cross reference file between SINGG/SUNGG galaxies and the IAU SN records
#SFTP_FILE               : A command file to fetch FITS images of SINGG/SUNGG galaxies
#STFP_IMG_PATH_FILE      : A text file containing the directory structure of all SINGG/SUNGG FITS images
#IMG_DIR                 : The location in which to download the fetched FITS images. Note this does not have to be in the OUT_DIR
#OVERLAY_DIR             : The absolute path in which the overlayed images will be saved into
#OVERLAY_RADIUS          : The radius of the overlay
#OVERLAY_SCRIPT          : The path to the shell script that automates the DS9 overlay process

IAU_URL                 = 'http://www.cbat.eps.harvard.edu/lists/Supernovae.html'
OUT_DIR                 = sys.argv[1]
SN_DB_FILE              = os.path.join(OUT_DIR, "out_supernovae_get.txt")
SN_TMP_FILE             = SN_DB_FILE + '.temp'
SN_POS_FILE             = re.sub('.txt', '_pos.txt', SN_DB_FILE)
MATCH_FILE              = os.path.join(OUT_DIR, "out_supernovae_match.csv")
STFP_FILE               = "/Users/21326604/Documents/gettingToKnowGalaxies/supernvoae/tmp/stfpFile"
#SFTP_FILE               = os.path.join(OUT_DIR, "out_sftp_batch")
STFP_IMG_PATH_FILE      = os.path.join('/Users/21326604/Documents/gettingToKnowGalaxies/supernovae/data/', 'g_glxy_fitsImgPaths.lis')
#IMG_DIR                 = '/media/kph/Seagate Backup Plus Drive/kphan/data/singg_supernovaeMatched_fits/'
IMG_DIR                 = "/Users/21326604/Documents/gettingToKnowGalaxies/supernovae/data/glxy_w_snII"
OVERLAY_DIR             = os.path.join(OUT_DIR, "overlay")
OVERLAY_RADIUS          = 0.0028
OVERLAY_SCRIPT          = "./supernovae_overlay_ds9.sh"
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
main()

#vim ts=4 sw=4

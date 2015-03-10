#!/bin/bash
#
#Author:        Khanh Phan
#Contact:       jme.ph2@gmail.com
#Last updated:  Tue March 10 2015
#This is a modular 'piece' of code in which will be run by a master script.
#Hence the galaxy in which the overlay is being produced is parsed through the
#command line arguments. An alternative to this is to introduce loops that
#iterate through a directory of input fits images and processes them
#accordingly.

#DS9 Parameters
RED_HIGH=0.0
RED_LOW=0.1
GREEN_HIGH=0.0
GREEN_LOW=0.7
BLUE_HIGH=0.0
BLUE_LOW=0.03
OUT_WIDTH=1920
OUT_HEIGHT=1080

#Command line arguments required to run DS9 script
GETDIR=$1       #Directory where images and regions files are located
OUTDIR=$2       #Directory where overlayed (output) images are saved
GALAXY=$3       #current working galaxy
RUN=$4          #run id of galaxy

#Move these files to the outdir for easy processing
#Note that these will be removed later in the script
cp "$GETDIR""$GALAXY"*"$RUN"'.fits' "$OUTDIR"

#Determine RGB fits file names through glob
GREEN_FITS_FILE=$(find $OUTDIR/ -name "$GALAXY"'_[1-9]*_ss_'"$RUN"'.fits')
RED_FITS_FILE=$OUTDIR/$GALAXY'_Rsub_ss_'$RUN'.fits'
BLUE_FITS_FILE=$OUTDIR/$GALAXY'_R_ss_'$RUN'.fits'
REGION_FILE=$GETDIR/$GALAXY'_regionfile.reg'
SAVE_FILE=$OUTDIR/$GALAXY'_overlay.jpg'

#DS9 prodcedure
./ds9 \
  -frame new rgb \
  -rgb system wcs \
  -rgb channel red \
  -rgb open $RED_FITS_FILE \
  -scale sqrt -scale limits $RED_LOW $RED_HIGH \
  -rgb channel green \
  -rgb open $GREEN_FITS_FILE \
  -scale sqrt -scale limits $GREEN_LOW $GREEN_HIGH \
  -rgb channel blue \
  -rgb open $BLUE_FITS_FILE \
  -scale sqrt -scale limits $BLUE_LOW $BLUE_HIGH \
  -regions load $REGION_FILE
  -rgb close \
  -view frame \
  -geometry $OUT_WIDTH'x'$OUT_HEIGHT \
  -width $OUT_WIDTH \
  -height $OUT_HEIGHT \
  -frame center \
  -zoom to fit \
  -saveimage jpeg $SAVE_FILE 100 \
  -exit

#remove temporarliy copied files
rm "$GREEN"
rm "$RED"
rm "$BLUE"

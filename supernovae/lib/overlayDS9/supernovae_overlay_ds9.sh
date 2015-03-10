#!/bin/bash

GETDIR=$1
OUTDIR=$2
GALAXY=$3
RUN=$4
REGIONFILE=' '


GREEN=$(find $OUTDIR/ -name "$GALAXY"'_[1-9]*_ss_'"$RUN"'.fits')
RED=$OUTDIR/$GALAXY'_Rsub_ss_'$RUN'.fits'
BLUE=$OUTDIR/$GALAXY'_R_ss_'$RUN'.fits'
cp "$GETDIR""$GALAXY"*"$RUN"'.fits' "$OUTDIR"

for GALAXY in $GETDIR; do
	cd ./$GALAXY
	GREEN=*'_avg.fits'
	BLUE=*'_-fd-int.fits'
	RED=*'_nd-int.fits'

	./ds9 \
	  -frame new rgb \
	  -rgb system wcs \
	  -rgb channel red \
	  -rgb open $RED \
	  -scale sqrt -scale limits 0.0 0.1 \
	  -rgb channel green \
	  -rgb open $GREEN \
	  -scale sqrt -scale limits 0.0 0.7 \
	  -rgb channel blue \
	  -rgb open $BLUE \
	  -scale sqrt -scale limits 0.0 0.03 \
	  -regions load $REGIONFILE
	  -rgb close \
	  -view frame \
	  -geometry 1920x1080 \
	  -width 1920 \
	  -height 1080 \
	  -frame center \
	  -zoom to fit \
	  -saveimage jpeg ./$GALAXY'_Overlay.jpeg' 100 \
	  -exit
	#rm "$GREEN"
	#rm "$RED"
	#rm "$BLUE"
done

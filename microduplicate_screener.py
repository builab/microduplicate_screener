#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Feb	5 17:35:42 2022

Micrograph duplicate screener
@author: kbui2
"""

import numpy as np
import errno, os, argparse
import starfile
import mrcfile

def binmicrograph(dfmicrograph, outdir, binning):
	''' Binning the micrograph'''
	for i in range(len(dfmicrograph)):
		bincmd = "newstack -bin {:d} {:s} {:s}".format(binning, dfmicrograph[i], outdir + '/' + os.path.basename(dfmicrograph[i]))
		print(bincmd)
		os.system(bincmd)
		

def tiltxcorr(ref, target, outdir):
	''' Correlate micrograph'''
	tiltxcorrcmd = "tiltxcorr -reference {:s} -input {:s} -output {:s}/out.xf -angles 0 -sigma1 0.03 -radius2 0.25 -sigma2 0.05".format(ref, target, outdir);
	print(tiltxcorrcmd)
	targetout = target.replace(".mrc", "_xf.mrc");
	shiftcmd = "newstack -in {:s} -ou {:s} -xform {:s}/out.xf".format(target, targetout, outdir);
	print(shiftcmd)
	os.system(tiltxcorrcmd)
	os.system(shiftcmd)
	
def bandpassfilter(im, outdir, lowpass, lpsigma, highpass, hpsigma):
	''' filtering micrograph. Change value to adjust'''
	imfil = im.replace(".mrc", "_fil.mrc")
	filtcmd = "mtffilter -input {:s} -output {:s} -lowpass {:0.2f},{:0.2f} -highpass {:0.2f},{:0.2f}".format(im, imfil, lowpass, lpsigma, highpass, hpsigma);
	print(filtcmd)
	os.system(filtcmd)
	return imfil
		


if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print("Remember to load IMOD before")
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--i', help='Input star file (from MotionCorr or CtfFind)',required=True)
	parser.add_argument('--outdir', help='Output folder (Temp)',required=False,default="dupscreener")
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--opticsless', help='With or without opticsgroup. Value 1 or 0',required=False,default="1")
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.25)

	args = parser.parse_args()
	
	#outdir= open(args.outdir, 'w')
	outdir = args.outdir
	binning = int(args.bin)
	screenrange = int(args.scanrange)
	threshold = float(args.threshold)
	


	try:
		os.mkdir(outdir)
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			raise
		pass
	
	stardict = starfile.read(args.i)
	if (args.opticsless == "1"):
		df = stardict
	else:
		df = stardict['micrographs']
		
	dfmicrograph = df["rlnMicrographName"].copy()
	
	#print(dfmicrograph)
	
	
	# Binning
	print("Binning data by {:d}".format(binning))
	binmicrograph(dfmicrograph, outdir, binning)
	
	ccc = np.zeros((len(dfmicrograph), screenrange), dtype=float);
	
	# loop through micrograph
	for i in range(len(dfmicrograph)):
		# Define range
		im = outdir + '/' + os.path.basename(dfmicrograph[i]);
		imfil = bandpassfilter(im, outdir, 0.25, 0.05, 0.04, 0.02)
		# Reading image
		immrc = mrcfile.open(imfil)
		print(immrc.data[10, 10])

		
		print("### Scanning duplicate for {:s} ###".format(im))
		if i + screenrange > len(dfmicrograph):
			topend = len(dfmicrograph)
		else:
			topend = i + screenrange
		
		for j in range(i+1, topend):
			target = outdir + '/' + os.path.basename(dfmicrograph[j])
			# Tiltxcorr
			tiltxcorr(im, target, outdir)
			# Filter target & return fil name
			targetfil = bandpassfilter(target, outdir, 0.25, 0.05, 0.04, 0.02)
			targetmrc = mrcfile.open(targetfil)
			# Corr correlation
			ccc[i, j-i-1] = np.corrcoef(immrc.data, targetmrc.data)
			targetmrc.close()
		immrc.close()
			
			
	
	numpy.savetxt("ccc.csv", ccc, delimiter=",")

		


	

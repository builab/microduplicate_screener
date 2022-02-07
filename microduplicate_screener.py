#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Feb	5 17:35:42 2022

Micrograph duplicate screener
@author: kbui2
"""

import numpy as np
import os
import starfile
import argparse
import mrcfile

def binmicrograph(dfmicrograph, binning):
	''' Binning the micrograph'''
	for i in len(dfmicrograph):
		bincmd = "newstack -bin {%d} {%s} {%s}".format(binning, dfmicrograph[i], outdir + '/' + dfmicrograph[i])
		print(bincmd)
		#os.system(bincmd)
		


if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.1 star file & McGill pattern of holes')
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--i', help='Input star file (from MotionCorr or CtfFind)',required=True)
 	parser.add_argument('--outdir', help='Output folder (Temp)',required=False, default='dupscreener')
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--opticsless', help='With or without opticsgroup. Value 1 or 0',required=False,default="1")
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.25)



	args = parser.parse_args()
	
	outdir= open(args.outdir, 'w')
 	binning = int(args.bin)
	screenrange = int(args.scanrange)
	threshold = float(args.threshold)
	
	
	
	stardict = starfile.read(args.i)
	if (args.opticsless == "1"):
		df = stardict
	else:
		df = stardict['micrographs']
		
	dfmicrograph = df["rlnMicrographName"].copy()
	
	
		
	
	# loop through micrograph
	for i in len(dfmicrograph):
		im = dfmicrograph[i]
		# Binning
		# Tiltxcorr
		cmd = sprintf('tiltxcorr -reference %s -input %s -output out.xf -angles 0 -sigma1 0.03 -radius2 0.25 -sigma2 0.05', im, targetim);

		filterim = 
				im = [imfile.folder '/' imfile.name];
		imfil = ['out/' strrep(imfile.name, '.mrc', '_fil.mrc')];
		targetim = [targetimfile.folder '/' targetimfile.name];
		targetfil = ['out/' strrep(targetimfile.name, '.mrc', '_fil.mrc')];
		cmd = sprintf('tiltxcorr -reference %s -input %s -output out.xf -angles 0 -sigma1 0.03 -radius2 0.25 -sigma2 0.05', im, targetim);
		targetout = ['out/' strrep(targetimfile.name, '.mrc', '_aln.mrc')];
		cmd2 = sprintf('newstack -in %s -ou %s -xform out.xf', targetim, targetout);
		cmd3 = sprintf('mtffilter -input %s -output %s -lowpass 0.25,0.05 -highpass 0.04,0.02', targetout, targetfil);
		cmd4 = sprintf('mtffilter -input %s -output %s -lowpass 0.25,0.05 -highpass 0.04,0.02', im, imfil);
		system(cmd);
		


	

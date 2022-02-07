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

def binmicrograph(dfmicrograph, outdir, binning):
	''' Binning the micrograph'''
	for i in range(len(dfmicrograph)):
		bincmd = "newstack -bin {:d} {:s} {:s}".format(binning, dfmicrograph[i], outdir + '/' + os.path.basename(dfmicrograph[i]))
		print(bincmd)
		#os.system(bincmd)
		


if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--i', help='Input star file (from MotionCorr or CtfFind)',required=True)
	parser.add_argument('--outdir', help='Output folder (Temp)',required=False,default="dupscreener")
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--opticsless', help='With or without opticsgroup. Value 1 or 0',required=False,default="1")
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.25)

	args = parser.parse_args()
	
	#outdir= open(args.outdir, 'w')
	outdir = 'dupsreener'
	binning = int(args.bin)
	screenrange = int(args.scanrange)
	threshold = float(args.threshold)
	
	stardict = starfile.read(args.i)
	if (args.opticsless == "1"):
		df = stardict
	else:
		df = stardict['micrographs']
		
	dfmicrograph = df["rlnMicrographName"].copy()
	
	print(dfmicrograph)
	
	
	# Binning
	print("Binning data by {:d}".format(binning))
	binmicrograph(dfmicrograph, outdir, binning)
	
	# loop through micrograph
	for i in range(len(dfmicrograph)):		
		# Tiltxcorr
		print('tiltxcorr')

		


	

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Feb	5 17:35:42 2022

Micrograph duplicate screener
@author: kbui2
"""

import numpy as np
import starfile
import argparse
import mrcfile


if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.1 star file & McGill pattern of holes')
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--i', help='Input star file (from MotionCorr or CtfFind)',required=True)
 	parser.add_argument('--outdir', help='Output folder (Temp)',required=True)
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--opticsless', help='With or without opticsgroup. Value 1 or 0',required=False,default="1")
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.25)



	args = parser.parse_args()
	
	
	imdir = open(args.imdir, 'r')
	outdir= open(args.outdir, 'w')
 	binning = int(args.bin)
	screenrange = int(args.scanrange)
	threshold = float(args.threshold)
	
	
	
	stardict = starfile.read(args.i)
	if (args.opticsless == 1):
		df = stardict
	else:
		df = stardict['micrographs']
		
	dfmicrograph = df["rlnMicrographName"]
	nosubtomo = len(dfmicrograph)
	
	# loop through micrograph
	for i in len(dfmicrograph):
		


	

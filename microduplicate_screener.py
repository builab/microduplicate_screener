#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Feb	5 17:35:42 2022

Micrograph duplicate screener
@author: kbui2
"""




if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.1 star file & McGill pattern of holes')
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--imdir', help='Input image folder',required=True)
  parser.add_argument('--outdir', help='Output folder (Temp)',required=True)
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.25)



	args = parser.parse_args()
	
	
	imdir = open(args.imdir, 'r')
	outdir= open(args.outdir, 'w')
 	binning = int(args.bin)
	screenrange = int(args.scanrange)
	threshold = float(args.threshold)

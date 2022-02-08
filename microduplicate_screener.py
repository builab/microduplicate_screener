#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Feb	5 17:35:42 2022

Micrograph duplicate screener
@author: kbui2
"""

import numpy as np
import multiprocessing as mp
import errno, os, argparse
import starfile
import mrcfile
import pandas as pd
import csv

def binmicrograph(dfmicrograph, outdir, binning):
	''' Binning the micrograph'''
	for i in range(len(dfmicrograph)):
		bincmd = "newstack -bin {:d} {:s} {:s}".format(binning, dfmicrograph[i], outdir + '/' + os.path.basename(dfmicrograph[i]))
		print(bincmd)
		os.system(bincmd)
		
def binsinglemicrograph(micrograph, outdir, binning):
	''' Binning the micrograph'''
	bincmd = "newstack -bin {:d} {:s} {:s}".format(binning, micrograph, outdir + '/' + os.path.basename(micrograph))
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
	
def bandpassfilter(im, outdir):
	''' filtering micrograph. Change value to adjust'''
	imfil = im.replace(".mrc", "_fil.mrc")
	filtcmd = "mtffilter -input {:s} -output {:s} -lowpass {:0.2f},{:0.2f} -highpass {:0.2f},{:0.2f}".format(im, imfil, LOWPASS, LPSIGMA, HIGHPASS, HPSIGMA);
	print(filtcmd)
	os.system(filtcmd)
	return imfil

def matchmicro(ref, target, outdir):
	# Tiltxcorr
	tiltxcorr(ref, target, outdir)
	# Filter target & return fil name
	imfil = bandpassfilter(ref, outdir)
	targetfil = bandpassfilter(target, outdir)
	immrc = mrcfile.open(imfil)
	targetmrc = mrcfile.open(targetfil)
	# Corr correlation
	r = np.corrcoef(immrc.data.flatten(), targetmrc.data.flatten())
	targetmrc.close()
	immrc.close()
	return r[1, 0]



if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print("Remember to load IMOD before")
	
	# CONSTANT
	LOWPASS=0.25
	LPSIGMA=0.05
	HIGHPASS=0.04
	HPSIGMA=0.02
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--i', help='Input star file (from MotionCorr or CtfFind)',required=True)
	parser.add_argument('--outdir', help='Output folder (Temp)',required=False,default="dupscreener")
	parser.add_argument('--csvout', help='CSV file of CCC',required=False,default="ccc.csv")
	parser.add_argument('--bin', help='Binning',required=False,default=8)
	parser.add_argument('--opticsless', help='With or without opticsgroup. Value 1 or 0',required=False,default="1")
	parser.add_argument('--scanrange', help='Range for scanning',required=False,default=48)
	parser.add_argument('--threshold', help='CCC threshold to set as duplicate',required=False,default=0.20)
	parser.add_argument('--j', help='Number of processors',required=False,default=1)


	
	args = parser.parse_args()
	
	outdir = args.outdir
	csvout = args.csvout
	nocpu = int(args.j)
	binning = int(args.bin)
	scanrange = int(args.scanrange)
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
		
	dfmicrograph = df["rlnMicrographName"].sort_values(ignore_index=True).copy()
	nomicro = len(dfmicrograph)
	#print(dfmicrograph)
	#exit(0)
	
	# Binning
	print("Binning data by {:d}".format(binning))
	pool = mp.Pool(nocpu)
	# Prep input, convert Series to Dataframe
	dfbin = dfmicrograph.to_frame()
	listoutdir = [outdir]*nomicro
	listbinning = [binning]*nomicro
	dfbin['Outdir'] = listoutdir
	dfbin['Binning'] = listbinning
	#print(dfbin)
	# Convert to tuple
	listbinargs = list(dfbin.itertuples(index=False, name=None))
	
	#print(listbinargs)

	# Parallel binning
	pool.starmap(binsinglemicrograph, listbinargs)
		
	duplist = {}
	csv_file = open(csvout, "w")
	writer = csv.writer(csv_file)
	
	# loop through micrograph
	for i in range(len(dfmicrograph)):
		# Define range
		im = outdir + '/' + os.path.basename(dfmicrograph[i]);
		# Create empty list
		listccc = [0]*scanrange
		scanlist = []
		
		
		print("### Scanning duplicate for {:s} ###".format(im))
		if i + scanrange > len(dfmicrograph):
			topend = len(dfmicrograph)
		else:
			topend = i + scanrange
		
		
		for j in range(i+1, topend):
			target = outdir + '/' + os.path.basename(dfmicrograph[j])
			scanlist.append(target)
			
		listim = [im]*(topend - i - 1)
		listoutdir = [outdir]*(topend - i - 1)
		
		# Check
		print(list(zip(listim, scanlist, listoutdir)))
		
		# Parallel
		result = pool.starmap(matchmicro, list(zip(listim, scanlist, listoutdir)))
		
		print(result)
		
		for x in range(len(result)): 
			listccc[x] = result[x]
			
		# Write CSV row
		writer.writerow(listccc)
		
		# Pick out the most similar one
		peak = np.argmax(listccc)
		print(peak)
		if list[peak] > threshold:
			duplist.append(i + peak + 1)
			
			
	

	csv_file.close()
	#np.savetxt("ccc.csv", ccc, delimiter=",", fmt='%.3f')
	dfmicrograph[duplist].to_csv('duplicate.csv')

	# Done parallel processing
	pool.close()
	pool.join()


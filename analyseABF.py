#! /usr/bin/python

from neo import io
import numpy as np
import sys
from matplotlib import pyplot as plt
import argparse
import peakutils

def findTimeIdx(arr,val):
	dvdt = []
	for i in range(50,len(arr)):
		dvdt.append(abs(arr[i]-arr[i-50]))
	p = dvdt.index(max(dvdt))
	cutoff = arr[p]+(val)
	for i in range(len(arr)):
		if arr[i]<cutoff:
			result = 1/200000.0*(i-p)*1000
			return [result,i,p]

def loadFile(filename):
	r = io.AxonIO(filename)
	bl = r.read_block(lazy=False, cascade=True)
	return bl
	
def plotTau(vals,t0,t1,tTau):
	plt.plot(vals)
	plt.axvline(x=t0)
	plt.axvline(x=t1)
	plt.axvline(x=tTau)
	plt.title(name)
	plt.show()

def findMin(vals):
	arr = []
	for i in range(10000,len(vals)):
		arr.append(np.mean(vals[i-10000:i]))
	print min(arr)
	plt.plot(arr)
	plt.show()
	return min(arr)

def getMinVal(bl):
	minVals = []
	for i in range(len(bl.segments)):
		seg = bl.segments[i]
		siglist = seg.analogsignals
		avg = np.mean(siglist, axis=0)
		maxVal = max(avg)
		minVal = min(avg)
		minVals.append(minVal)
	idx =  minVals.index(min(minVals))
	arr = np.mean(bl.segments[idx].analogsignals, axis=0).tolist()

	tidx = arr.index(min(minVals))
	val = (arr[tidx]-arr[0])/3
#	print "Slice: %s, minVal:%s, startVal:%s, constant:%s" % (idx,arr[tidx],arr[0],val)
#	print "-"*80
	var,i,p =  findTimeIdx(arr[:10000],val)
###
#	newval = (findMin(arr)-arr[0])/3
#	n1,n2,n3 = findTimeIdx(arr[:10000],newval)
#	print n1
	plotTau(arr,p,i,tidx)
	return var

def timeConstant(filename):
	global name
	name = args.filename.split("/")[-1]
	bl = loadFile(args.filename)
	print "-"*80
	var = getMinVal(bl)	
	print("%s\t%s" % (name,var))

def findPeaks(bl):
	sliceNum = 0
	for s in bl.segments:
		sliceNum += 1
		sig = np.mean(s.analogsignals,axis=0)

		if max(sig)<0:
			continue
		dsArr = []
		for i in range(0,len(sig),100):
			dsArr.append(sig[i])
		cb = np.array(dsArr)
		idx = peakutils.indexes(cb)
		plt.plot(cb)
		for i in idx:
			plt.axvline(x=i)
		plt.show()
		print("%s\t%s" % (sliceNum,len(idx)))

def peaks(args):
	global name
	name = args.filename.split("/")[-1]
	bl = loadFile(args.filename)
	findPeaks(bl)



parser = argparse.ArgumentParser(description='Next-generation sequencing processing pipeline for the rasberry pi',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(help="Task to perform")

parser_tc = subparsers.add_parser('tau', help='Use minia to assemble reads',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_tc.add_argument('filename',help='File name')
parser_tc.set_defaults(func=timeConstant)

parser_dp = subparsers.add_parser('peaks', help='Use minia to assemble reads',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser_dp.add_argument('filename',help='File name')
parser_dp.set_defaults(func=peaks)


args = parser.parse_args()
args.func(args)

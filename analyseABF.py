#! /usr/bin/python

from neo import io
import numpy as np
import sys
from matplotlib import pyplot as plt

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
	plt.show()

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
	print "Slice: %s, minVal:%s, startVal:%s, constant:%s" % (idx,arr[tidx],arr[0],val)
	print "-"*80
	var,i,p =  findTimeIdx(arr[:10000],val)
	plotTau(arr,p,i,tidx)
	return var

def main(filename):
	bl = loadFile(filename)
	var = getMinVal(bl)
	print var


main(sys.argv[1])

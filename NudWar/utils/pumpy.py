"""
"pumpy" stands for pebble numpy. Any math functions I don't want to store somewhere else go here
"""

import numpy as np # my dad

def distanceFormula(pos1: tuple[float], pos2: tuple[float]):
	x = pos2[0]-pos1[0]
	y = pos2[1]-pos1[1]
	return np.sqrt(x*x+y*y)

def manhatten(pos1: tuple[float], pos2: tuple[float]):
	return np.abs(pos2[0]-pos1[0])+np.abs(pos2[1]-pos1[1])

def divideVectors(vecA: tuple[float], vecB: tuple[float]):
	n = vecB[0]*vecB[0]+vecB[1]*vecB[1]
	return [
		(vecA[0]*vecB[0]+vecA[1]*vecB[1])/n,
		(vecA[1]*vecB[0]-vecA[0]*vecB[1])/n
	]

def dotProductSum(vecA: tuple[float], vecB: tuple[float]):
	return vecA[0]*vecB[0]+vecA[1]*vecB[1]

def crossProductDifference(vecA: tuple[float], vecB: tuple[float]):
	return vecA[0]*vecB[1]-vecA[1]*vecB[0]

def AngleBetweenTwoUnitVectors(vecA: tuple[float], vecB: tuple[float]):
	"""
	This method skips calculating vector magnitudes to save time on calculation.
	"""
	return np.degrees(np.arccos(dotProductSum(vecA, vecB)))

def normalizeVector(vec: tuple[float]):
	d = np.sqrt(vec[0]*vec[0]+vec[1]*vec[1])

	return [vec[0] / d, vec[1] / d]

if __name__ == "__main__":
	nud = (-0.92, -0.37)
	target = (0.93, -0.35)

	print(divideVectors(target, nud))
import os
import numpy as np
from tqdm import tqdm
from itertools import combinations_with_replacement
from sympy.utilities.iterables import multiset_permutations

path = ''

s = [-1, 0, 1]
n = len(s)

ks = list(range(1, 11))


for k in tqdm(ks):

	I = [[] for _ in range(n**k)]
	cs = combinations_with_replacement(s, k)
	li = 0
	ts = []
	for c in cs:
		ps = list(multiset_permutations(c))
		l = len(ps)
		for i,p in enumerate(ps):
			I[li+i] = p
		li += l
	
	I = np.array(I, dtype=np.int8)
	np.save(os.path.join(path, 'cwr_' + str(k) + '.npy'), I)

import os
import json
import math
import sys
import numpy as np
import pandas as ps
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from itertools import combinations_with_replacement, permutations
from sympy.utilities.iterables import multiset_permutations




path = ''
files = sorted(os.listdir(path))

ois = np.empty((0,2))
for file in files:
	with open(os.path.join(path, file)) as f:
		data = json.load(f)
	o = np.empty((len(data),2))
	for i,d in enumerate(data):
		o[i] = [d['time'], float(d['openInterest'])]
	ois = np.vstack((ois, o))

dtnz = np.where(np.diff(ois[:,0]) != 0)[0]
ois = ois[dtnz]

times_o = ois[:,0]
intervals_o = [(times_o[i-1], times_o[i]) for i in range(1,len(times_o))]


trades = ps.read_csv('/Users/jonkqiku/Downloads/ATOMUSDT-trades-2023-12-01.csv')
trades['is_buyer_maker'] = trades['is_buyer_maker'].astype(int)
trades = trades[['time', 'qty', 'price', 'is_buyer_maker']].to_numpy()

t0 = ois[0,0]
t1 = ois[-1,0]
a = np.where(trades[:,0] > t0)[0][0]
b = np.where(trades[:,0] > t1)[0][0]
trades = trades[a:b]

times_t = trades[:,0]

trades_idxs = []
i = 0
for it in intervals_o:
	idxs = []
	while i < len(trades) and times_t[i] > it[0] and times_t[i] <= it[1]:
		idxs.append(i)
		i += 1
	trades_idxs.append(idxs)

doi = np.diff(ois[:,1])
adoi = abs(doi)

itv = np.empty(len(trades_idxs))
for i, it in enumerate(trades_idxs):
	if len(it) > 0:
		v = trades[it,1].sum()
	else:
		v = 0
	itv[i] = v






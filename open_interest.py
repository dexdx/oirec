import os
import requests
import numpy as np
from time import time

path = ''

base =  'https://fapi.binance.com'
exts = {'oi': '/futures/data/openInterestHist',
        'mark': '/fapi/v1/markPriceKlines',
        'lsr': '/futures/data/globalLongShortAccountRatio'}

symbol = 'TRXUSDT'
period = '5m'
params = {'oi': {'symbol': symbol, 'period': period, 'limit': 500},
          'mark': {'symbol': symbol, 'interval': period, 'limit': 1500},
          'lsr': {'symbol': symbol, 'period': period, 'limit': 500}}

vars = exts.keys()
ts = str(round(time()*1000))

def process_oi(resp):
    ois = np.empty((len(resp), 3))
    for i,o in enumerate(resp):
        t = float(o['timestamp'])
        oiq = float(o['sumOpenInterest'])
        oiv = float(o['sumOpenInterestValue'])
        ois[i] = [t, oiq, oiv]
    return ois

def process_mark(resp):
    mark = np.empty((len(resp), 6))
    for i,o in enumerate(resp):
        ot = o[0]
        po = o[1]
        hi = o[2]
        lo = o[3]
        pc = o[4]
        ct = o[6]
        mark[i] = [ot, ct, po, hi, lo, pc]
    return mark

def process_lsr(resp):
    lsr = np.empty((len(resp), 3))
    for i,o in enumerate(resp):
        t = float(o['timestamp'])
        l = float(o['longAccount'])
        s = float(o['shortAccount'])
        lsr[i] = [t, l, s]
    return lsr


def process(resp, var):
    if var == 'oi':
        return process_oi(resp)
    elif var == 'mark':
        return process_mark(resp)
    elif var == 'lsr':
        return process_lsr(resp)


for var in vars:
    resp = requests.get(base + exts[var], params=params[var])

    if resp.ok:
        print(f'{var.upper()} request succeeded')
        name = '_'.join([symbol, var, period, ts]) + '.npy'
        resp = resp.json()
        data = process(resp, var)
        np.save(os.path.join(path, name), data)
    else:
        print(f'{var.upper()} request failed')


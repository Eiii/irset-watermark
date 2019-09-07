#!/usr/bin/env python3

import argparse
import sys
from struct import unpack
from random import getrandbits as grb


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('text', nargs='?', default=None)
    parser.add_argument('output', nargs='?', default='out.sto')
    return parser


def kf(k=0):
    while True:
        k = (k+0xf0)*0xfb % 0xff
        yield k


def verify(fd):
    magic, fs = unpack('<II', fd.read(8))
    if magic != 0x0003:
        print('Not an iRacing setup file.')
        sys.exit()
    return fs


def extract(fd):
    fs = verify(fd)
    fd.seek(fs+8)
    w = fd.read()
    if len(w) < 10:
        return
    k1, k2, w, z = w[0], w[1], w[2:-8], w[-8:]
    if unpack('Q', z) != (0,):
        return
    return bytes(v ^ k for v, k in zip(w, kf(k1 ^ k2))).decode()


def put(fd, s, out):
    fs = verify(fd)
    fd.seek(0)
    out.write(fd.read(fs+8))
    if s:
        k1, k2 = grb(8), grb(8)
        out.write(bytes([k1, k2]))
        out.write(bytes(v ^ k for k, v in zip(s.encode(), kf(k1 ^ k2))))
    out.write(bytes(8))
    if s:
        print(f'Added watermark `{s}`')
    else:
        print('Removed watermark')


args = make_parser().parse_args()
if args.text is not None:
    with open(args.path, 'rb') as fd:
        with open(args.output, 'wb') as fd_out:
            put(fd, args.text, fd_out)
else:
    with open(args.path, 'rb') as fd:
        wm = extract(fd)
        if wm:
            print('Watermark:')
            print(wm)
        else:
            print('No watermark')

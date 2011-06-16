#!/usr/bin/env python2
import jsonpickle # 1
import cPickle # 2
import pickle # 3
from time import time
import os, sys

import psutil

def usage():
    print sys.argv[0] + " 1/2/3 (resp: jsonpickle, cPickle, pickle) [ if pickle/cpickle: proto. 0/1/2]"

def save(obj, fname, m, proto):
    with open(fname, 'w') as fout:
        if m == 1:
            fout.write(jsonpickle.encode(obj))
        if m == 2:
            cPickle.dump(obj, fout, proto)
        if m == 3:
            pickle.dump(obj, fout, proto)

def load(fname, m):
    with open(fname, 'r') as fin:
        if m == 1:
            return jsonpickle.decode(fin.read())
        if m == 2:
            return cPickle.load(fin)
        if m == 3:
            return pickle.load(fin)

def getinfo ():
    return time (), p.get_memory_info().rss / 1000000.0

def getstats (A_time, B_time, A_mem, B_mem, fname):
    duration = B_time - A_time
    size = os.path.getsize(fname) / 1000000.0
    speed = size / duration
    rss_diff = B_mem - A_mem
    rss_diff_per_filesize = rss_diff / size
    return duration, size, speed, rss_diff, rss_diff_per_filesize

if len(sys.argv) < 2 or int(sys.argv[1]) not in [1, 2, 3]:
    usage()
    sys.exit(1)
m = int(sys.argv[1])
proto = 0
if len(sys.argv) > 2:
    proto = int(sys.argv[2])
    if proto not in [0, 1, 2]:
        usage()
        sys.exit(1)

pid = os.getpid()
p = psutil.Process(pid)
d = {}
test_point = 1000 # will get increased in larger amounts at each point
i = 0
string = 'aeuaeuaoeusthsthshtaeuaseuthaeuasetuhaeou'

titles = ['JsonPickle', 'cPickle', 'pickle']
print "Testing", titles[m-1]
if m > 1:
	print "Protocol", proto

while True:
    i += 1
    d[i] = string
    if i == test_point:
        print "== %i ==" %i
        fname = 'dict-%s' %i
        A_time, A_mem = getinfo()
        save(d, fname, m, proto)
        B_time, B_mem = getinfo()
        duration, size, speed, rss_diff, rss_diff_per_filesize = getstats (A_time, B_time, A_mem, B_mem, fname)
        print "Stored in %.2fs. file size %.2f MB. Speed %.2f MB/s. RSS taken %.2f MB. (%.2f MB per MB in file)" % (duration, size, speed, rss_diff, rss_diff_per_filesize)

        A_time, A_mem = getinfo()
        d = load (fname, m)
        B_time, B_mem = getinfo()
        duration, size, speed, rss_diff, rss_diff_per_filesize = getstats (A_time, B_time, A_mem, B_mem, fname)
        print "Loaded in %.2fs. Speed %.2f MB/s. RSS taken %.2f MB.  (%.2f MB per MB in file)" % (duration, speed, rss_diff, rss_diff_per_filesize)
        test_point *= 4
        # a health check to be sure:
        if m == 1:
            # workaround for https://github.com/jsonpickle/jsonpickle/issues/5
            verify = d[str(i)]
        else:
            verify = d[i]
        if verify != string:
            sys.stderr.write("ERROR. d[%i] = %s, should be %s", i, str(d[i], string))
            sys.exit(2)

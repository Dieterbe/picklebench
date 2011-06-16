#!/bin/bash
./pickletest.py 1   > output-1
./pickletest.py 2 0 > output-2-proto0
./pickletest.py 2 1 > output-2-proto1
./pickletest.py 2 2 > output-2-proto2
./pickletest.py 3 0 > output-3-proto0
./pickletest.py 3 1 > output-3-proto1
./pickletest.py 3 2 > output-3-proto2

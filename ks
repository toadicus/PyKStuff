#!/bin/bash

scriptdir=$(dirname $(readlink -f $0))

python3 "$scriptdir"/PyKStuff.py $*
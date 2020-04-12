#!/usr/bin/zsh

set -ve

test -d tmp || mkdir tmp

pushd tmp
../packetlib.py ../packet.yaml
cat packet.h
popd

gccr struct.c

python send.py

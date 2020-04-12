#!/usr/bin/zsh

set -v

pushd tmp
../packetlib.py ../packet.yaml
cat packet.h
popd

gccr struct.c

python send.py

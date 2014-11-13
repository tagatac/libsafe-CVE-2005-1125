#!/usr/bin/env bash

#With interposition
LD_PRELOAD=libsafe-2.0-16/src/libsafe.so:$(pwd)/interpose.so timing/baseline-test $1

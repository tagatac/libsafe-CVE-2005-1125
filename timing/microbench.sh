#!/usr/bin/env bash

cd ..
echo Without interposition
echo =====================
LD_PRELOAD=libsafe-2.0-16/src/libsafe.so timing/baseline-test $1
echo
echo With interposition
echo ==================
LD_PRELOAD=libsafe-2.0-16/src/libsafe.so:$(pwd)/interpose.so timing/baseline-test $1

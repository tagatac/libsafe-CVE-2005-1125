#!/usr/bin/env bash

export LD_PRELOAD=libsafe-2.0-16/src/libsafe.so:$(pwd)/interpose.so
./thread

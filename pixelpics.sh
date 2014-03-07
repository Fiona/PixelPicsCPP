#!/bin/sh

LIBS=./libs
BIN=./bin/pixelpics

# Run your app
export LD_LIBRARY_PATH=$LIBS:"$LD_LIBRARY_PATH"
$BIN $@

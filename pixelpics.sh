#!/bin/sh

LIBS=./libs
BIN=./bin/pixelpics

# Work around for touchpads being too fast in fullscreen mode
export SDL_MOUSE_RELATIVE=0

# Run pix run
export LD_LIBRARY_PATH=$LIBS:"$LD_LIBRARY_PATH"
$BIN $@

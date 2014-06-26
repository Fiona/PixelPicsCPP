#!/bin/sh

if [ `getconf LONG_BIT` = "64" ]
then
    LIBS=./libs/x86_64
    BIN=./bin/x86_64/pixelpics
else
    LIBS=./libs/i386
    BIN=./bin/i386/pixelpics
fi

# Work around for touchpads being too fast in fullscreen mode
export SDL_MOUSE_RELATIVE=0

# I hate SDL mixers garbage. I hate audio on linux more.
export SDL_AUDIODRIVER=alsa pulse audio

# Run pix run
export LD_LIBRARY_PATH=$LIBS:"$LD_LIBRARY_PATH"
$BIN $@

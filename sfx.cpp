/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Sound effects loading 
 ****************************/


#include <string>
#include <iostream>
#include "main.h"
using namespace std;


SFX::SFX()
{

    sound = NULL;

}


SFX::SFX(string sound_file)
{

    sound = Mix_LoadWAV(sound_file.c_str());

}


SFX::~SFX()
{

    Mix_FreeChunk(sound);

}


void SFX::play(int times_repeat)
{

    Mix_PlayChannel(-1, sound, times_repeat);

}

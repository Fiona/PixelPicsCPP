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

    game = NULL;
    sound = NULL;
    channel = -1;

}


SFX::SFX(string sound_file, Main_App* _game, bool _overlap)
{

    game = _game;
    overlap = _overlap;
    sound = Mix_LoadWAV(sound_file.c_str());
    channel = -1;

}


SFX::~SFX()
{

    Mix_FreeChunk(sound);

}


void SFX::play(int times_repeat)
{

    if(game->settings->sound_effects_vol <= 10 || !game->settings->sound_effects_on)
        return;

    if(!overlap && channel != -1)
        return;

    Mix_VolumeChunk(sound, game->settings->sound_effects_vol);
    channel = Mix_PlayChannel(-1, sound, times_repeat);

}

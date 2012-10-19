/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Sound effects loading header
 ****************************/

#ifndef _SFX_H_
#define _SFX_H_
 
#include <string>
using namespace std;

#include <SDL/SDL.h>
#include <SDL/SDL_mixer.h>

#include "main.h"

class Main_App;

/*
 */ 
class SFX
{

public:
    SFX();
    SFX(string sound_file, Main_App* _game, bool overlap = True);
    ~SFX();
    void play(int times_repeat = 0);

    int channel;
    bool overlap;

private:
    Main_App* game;
    Mix_Chunk *sound;

};
 
#endif

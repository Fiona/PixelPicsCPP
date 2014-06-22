/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Music loading and playing header
 ****************************/

#ifndef _MUSIC_H_
#define _MUSIC_H_
 
#include <string>
using namespace std;

#include <SDL/SDL.h>
#include <SDL/SDL_mixer.h>

#include "main.h"

class Main_App;

/*
 */ 
class Music
{

public:
    Music();
    Music(string sound_file, Main_App* _game);
    ~Music();
    void play_loop(int fade_out_time = 1000);
    void play(int fade_out_time = 1000);
    void stop(int fade_out_time);
    void set_volume(int volume);

private:
    Main_App* game;
    Mix_Music *sound;

};
 
#endif

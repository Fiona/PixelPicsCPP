/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Music loading and playing
 ****************************/


#include <string>
#include <iostream>
#include "main.h"
using namespace std;


Music::Music()
{

    game = NULL;
    sound = NULL;

}


Music::Music(string sound_file, Main_App* _game)
{

    game = _game;
    sound = Mix_LoadMUS(sound_file.c_str());

}


Music::~Music()
{

    Mix_FreeMusic(sound);

}


void Music::play_loop(int fade_out_time)
{

    if(game->settings->music_vol <= 10 || !game->settings->music_on)
        return;

    if(game->current_playing_music != NULL)
        game->current_playing_music->stop(fade_out_time);

    game->current_playing_music = this;

    Mix_VolumeMusic(game->settings->music_vol);
    Mix_PlayMusic(sound, -1);

}


void Music::stop(int fade_out_time)
{

    if(!Mix_PlayingMusic())
        return;
    Mix_FadeOutMusic(fade_out_time);

}


void Music::set_volume(int volume)
{
    Mix_VolumeMusic(volume);
}

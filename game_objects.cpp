/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Game objects
 ****************************/


#include "game_objects.h"

#include <iostream>


Ship::Ship(Main_App* _game, float pos_x, float pos_y): Process()
{
    x = pos_x;
    y = pos_y;
    game = _game;
    image = game->media->gfx["ship"];
}

void Ship::Execute()
{
    if(game->Keyboard_key_down(SDLK_LEFT))
        x -= 10.0;
    if(game->Keyboard_key_down(SDLK_RIGHT))
        x += 10.0;
    if(game->Keyboard_key_down(SDLK_UP))
        y -= 10.0;
    if(game->Keyboard_key_down(SDLK_DOWN))
        y += 10.0;
}


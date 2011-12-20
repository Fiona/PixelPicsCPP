/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Game objects
 ****************************/


#include "game_objects.h"


Ship::Ship(Main_App* game, float pos_x, float pos_y): Process()
{
    x = pos_x;
    y = pos_y;
    game = game;
    image = game->media->gfx["ship"];
}


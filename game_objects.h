/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Game objects header
 ****************************/

#ifndef _GAME_OBJECTS_H_
#define _GAME_OBJECTS_H_

#include "main.h"


class Main_App;


/*
 */
class Ship: public Process
{

private:
    Main_App* game;

public:
    Ship(Main_App* game, float pos_x, float pos_y);

};


#endif

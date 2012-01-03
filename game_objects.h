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
    void Execute();

};


/*
 */
class Main_input: public Process
{

private:
    Main_App* game;
    void create_vorticies(float x, float y, int type);
    int current_rotation;
    int current_rotation_2;

public:
    Main_input(Main_App* game);
    void Execute();

    Text* current_fps_display;
    Text* current_process_count_display;

};


class Shot: public Process
{

private:
    Main_App* game;
    int rotation_to;

public:
    Shot(Main_App* game, float x, float y, int rotation_to);
    void Execute();

};

#endif

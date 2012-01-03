/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Processesss source file
 ****************************/


#include "main.h"
#include <iostream>
#include <math.h>
 

std::vector<Process*> Process::Process_List;
std::vector<Process*> Process::Processes_to_kill;
bool Process::z_order_dirty;

 
Process::Process()
{
    x = y = 0.0f;
    z = 0;
    image = NULL;
    Process::z_order_dirty = True;
    Process::Process_List.push_back(this);
}


Process::~Process()
{
}


void Process::Execute()
{
}


void Process::Draw(SDL_Surface* screen)
{

    if(image == NULL || screen == NULL)
        return;

    SDL_Rect rect;
    tuple<float, float> draw_pos = get_screen_draw_position();
    rect.x = draw_pos.get<0>();
    rect.y = draw_pos.get<1>();

    SDL_BlitSurface(image->surface, NULL, screen, &rect);

}


void Process::Kill()
{
    Process::Processes_to_kill.push_back(this);
}


void Process::move_forward(float distance_to_travel, int rotation_to_move_in)
{
    x = x + distance_to_travel * cos(deg_to_rad(rotation_to_move_in));
    y = y + distance_to_travel * sin(deg_to_rad(rotation_to_move_in));
}


float Process::deg_to_rad(float deg)
{
    return (3.1415926f / 180.0f) * deg;
}
 

float Process::rad_to_deg(float rad)
{
    return rad * 180.0f / 3.1415926f;
}


tuple<float, float> Process::get_screen_draw_position()
{

    if(image == NULL)
        return tuple<float, float>(x, y);

    return tuple<float, float>(x - (image -> width / 2), y - (image -> height / 2));

}

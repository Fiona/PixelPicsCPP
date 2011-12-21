/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Processesss source file
 ****************************/


#include "main.h"
#include <iostream>
 

std::vector<Process*> Process::Process_List;
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
    rect.x = x;
    rect.y = y;

    SDL_BlitSurface(image->surface, NULL, screen, &rect);

}

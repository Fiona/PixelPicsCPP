/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Render loop 
 ****************************/


#include "main.h"
#include "process.h"
#include <iostream>
#include <algorithm>

bool sort_by_z(Process* i, Process* j)
{
    return ((*i).z > (*j).z);
}

 
void Main_App::On_Render()
{

    // Re sort by Z value
    if(Process::z_order_dirty)
    {
        sort(Process::Process_List.begin(), Process::Process_List.end(), sort_by_z);
        Process::z_order_dirty = False;
    }

    // clear screen
    SDL_Rect screen_rect = {0,0,640,480};
    SDL_FillRect(surf_display, &screen_rect, 0);

    // Draw in order of z value
    for(std::vector<Process*>::iterator it = Process::Process_List.begin(); it != Process::Process_List.end(); ++it)
    {

        if(*it == NULL)
            continue;
 
        (*it)->Draw(surf_display);

    }

    // Flippy
    SDL_Flip(surf_display);

}


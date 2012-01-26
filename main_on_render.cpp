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
    glClear(GL_COLOR_BUFFER_BIT);

    // Set up pre-drawing
    glEnableClientState(GL_VERTEX_ARRAY);
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);
    glTexCoordPointer(2, GL_FLOAT, 0, &Process::default_texture_coords[0]);

    // Draw in order of z value
    for(std::vector<Process*>::iterator it = Process::Process_List.begin(); it != Process::Process_List.end(); ++it)
    {

        if(*it == NULL || (*it)->is_dead == True)
            continue;

        // Call custom strategy if necessary
        if((*it)->draw_strategy == "")
            (*it)->Draw();
        else
        {
            map<std::string, FuncGetter>::iterator found = draw_strategies.find((*it)->draw_strategy);
            if(found != draw_strategies.end())
            {
                FuncGetter func = found->second;
                ((*it)->*func)();
            }
        }

    }

    // Disable gl stuff and flip buffer
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glDisableClientState(GL_VERTEX_ARRAY);
    SDL_GL_SwapBuffers();

}


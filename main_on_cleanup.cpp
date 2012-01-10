/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Hoover file
 ****************************/

#include "main.h"
 
void Main_App::On_Cleanup()
{

    // Bye Bye SDL
    SDL_Quit();
/*
    // Clean up processes
    for(std::vector<Process*>::iterator it = Process::Process_List.begin(); it != Process::Process_List.end(); ++it)
    {
        if(*it == NULL)
            continue;
        delete *it;
        *it = NULL;
    }
*/
    // Kill all the loaded media items
    delete media;

}

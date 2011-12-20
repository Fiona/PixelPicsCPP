/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Render loop 
 ****************************/


#include "main.h"
#include "process.h"

 
void Main_App::On_Render()
{

    for(std::vector<Process*>::iterator it = Process::Process_List.begin(); it != Process::Process_List.end(); ++it)
    {

        if(*it == NULL)
            continue;
 
        (*it)->Draw(surf_display);

    }

    SDL_Flip(surf_display);

}

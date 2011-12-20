/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main game loop 
 ****************************/

#include "main.h"
 
void Main_App::On_Loop()
{

    for(std::vector<Process*>::iterator it = Process::Process_List.begin(); it != Process::Process_List.end(); ++it)
    {

        if(*it == NULL)
            continue;
 
        (*it)->Execute();

    }

}

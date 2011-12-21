/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main game loop 
 ****************************/

#include "main.h"
#include <iostream>

 
void Main_App::On_Loop()
{

    std::vector<Process*> copy_list(Process::Process_List);

    for(std::vector<Process*>::iterator it = copy_list.begin(); it != copy_list.end(); ++it)
    {

        if(*it == NULL)
            continue;
 
        (*it)->Execute();

    }

}

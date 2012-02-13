/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main game loop 
 ****************************/

#include "main.h"
#include <iostream>


bool sort_by_priority(Process* i, Process* j)
{
    return ((*i).priority > (*j).priority);
}


 
void Main_App::On_Loop()
{

    // Re sort by priority value
    if(Process::priority_order_dirty)
    {
        sort(Process::Priority_List.begin(), Process::Priority_List.end(), sort_by_priority);
        Process::priority_order_dirty = False;
    }

    vector<Process*>::iterator dead_check;

    std::vector<Process*> copy_list(Process::Priority_List);
    //std::vector<Process*> copy_list(Process::Process_List);

    for(std::vector<Process*>::iterator it = copy_list.begin(); it != copy_list.end(); ++it)
    {

        dead_check = std::find(Process::Processes_to_kill.begin(), Process::Processes_to_kill.end(), *it);

        if(*it == NULL || (*it)->is_dead == True)
            continue;

        if(dead_check != Process::Processes_to_kill.end())
            continue;

        try
        {
            (*it)->Execute();
        }
        catch(boost::python::error_already_set const &)
        {
            PyErr_Print();
            cout << "Error from Python interpreter. Bailing out." << endl;
            Quit();
        }

    }
    
    /*
    if(Keyboard_key_down(SDLK_ESCAPE))
        Quit();
    */

}

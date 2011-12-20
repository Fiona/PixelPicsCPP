/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Event handler loop
 ****************************/

#include "main.h"
 
void Main_App::On_Event(SDL_Event* Event)
{

    if(Event->type == SDL_QUIT)
        running = False;

}

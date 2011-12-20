/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Event handler loop
 ****************************/

#include "main.h"

#include <iostream>
#include <vector>
#include <algorithm> 

void Main_App::On_Event(SDL_Event* Event)
{

    if(Event->type == SDL_QUIT)
        running = False;

    switch(Event->type)
    {
    
    case SDL_KEYDOWN:
        Keyboard_keys_down.push_back(Event -> key.keysym.sym);
        break;
 
    case SDL_KEYUP:
        vector<SDLKey>::iterator it;
        it = std::find(Keyboard_keys_down.begin(), Keyboard_keys_down.end(), Event -> key.keysym.sym);
        if(it != Keyboard_keys_down.end())
            Keyboard_keys_down.erase(it);
        break;

    }

}

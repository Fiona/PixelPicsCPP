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
        if(text_input_enabled)
            Text_input.push_back(Event->key.keysym.unicode);
        break;
 
    case SDL_KEYUP:
    {
        vector<SDLKey>::iterator it;
        it = std::find(Keyboard_keys_down.begin(), Keyboard_keys_down.end(), Event -> key.keysym.sym);
        if(it != Keyboard_keys_down.end())
            Keyboard_keys_down.erase(it);
        Keyboard_keys_released.push_back(Event -> key.keysym.sym);
        break;
    }

    case SDL_MOUSEMOTION:
        mouse->x = Event->motion.x;
        mouse->y = Event->motion.y;
        mouse->x_rel = Event->motion.xrel;
        mouse->y_rel = Event->motion.yrel;
        break;

    case SDL_MOUSEBUTTONDOWN:
        switch(Event->button.button)
        {
        case SDL_BUTTON_LEFT:
            mouse->left_down = True;
            break;
        case SDL_BUTTON_RIGHT:
            mouse->right_down = True;
            break;
        case SDL_BUTTON_MIDDLE:
            mouse->middle_down = True;
            break;
        case SDL_BUTTON_WHEELUP:
            mouse->wheel_up = True;
            break;
        case SDL_BUTTON_WHEELDOWN:
            mouse->wheel_down = True;
            break;
        }
        break;

    case SDL_MOUSEBUTTONUP:
        switch(Event->button.button)
        {
        case SDL_BUTTON_LEFT:
            mouse->left_down = False;
            mouse->left_up = True;
            break;
        case SDL_BUTTON_RIGHT:
            mouse->right_down = False;
            mouse->right_up = True;
            break;
        case SDL_BUTTON_MIDDLE:
            mouse->middle_down = False;
            mouse->middle_up = True;
            break;
        }
        break;

    }

}

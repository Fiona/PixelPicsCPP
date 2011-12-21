/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app file
 ****************************/

#include <iostream>
#include <vector>
#include <algorithm> 
using namespace std;

#include "main.h"


Main_App::Main_App()
{

    surf_display = NULL;
    running = True;
    desired_fps = 60;
    delay_ticks = 0;

}

 
int Main_App::On_Execute()
{

    if(On_Init() == False)
    {
        return -1;
    }
 
    SDL_Event event;

    desired_fps = 60;
 
    while(running)
    {

        while(SDL_PollEvent(&event))
            On_Event(&event);

        On_Loop();
        On_Render();
        
        Wait_till_next_frame();

    }
 
    On_Cleanup();
 
    return 0;

}
 

bool Main_App::Keyboard_key_down(SDLKey Key)
{

    vector<SDLKey>::iterator it = std::find(Keyboard_keys_down.begin(), Keyboard_keys_down.end(), Key);
    if(it != Keyboard_keys_down.end())
        return True;      
    return False;

}



void Main_App::Wait_till_next_frame()
{

    if((SDL_GetTicks() - delay_ticks) < 1000 / desired_fps)
        SDL_Delay((1000 / desired_fps) - (SDL_GetTicks() - delay_ticks));

    delay_ticks = SDL_GetTicks();

}



int main(int argc, char* argv[])
{

    Main_App app;
    return app.On_Execute();

}

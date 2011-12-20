/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app file
 ****************************/

#include <iostream>
using namespace std;
#include "main.h"


Main_App::Main_App()
{

    surf_display = NULL;
    running = True;

}

 
int Main_App::On_Execute()
{

    if(On_Init() == False)
    {
        return -1;
    }
 
    SDL_Event event;
 
    while(running)
    {

        while(SDL_PollEvent(&event))
            On_Event(&event);
 
        On_Loop();
        On_Render();

    }
 
    On_Cleanup();
 
    return 0;

}
 

int main(int argc, char* argv[])
{

    Main_App app;
    return app.On_Execute();

}

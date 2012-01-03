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
    current_fps = 0;
    frames_rendered = 0;
    for(uint x = 0; x < 8; x++)
        default_texture_coords[x] = 0.0f;
}

 
int Main_App::On_Execute()
{

    if(On_Init() == False)
        return -1;
 
    SDL_Event event;

    desired_fps = 60;
    frames_rendered = 0;
    current_fps = 0;
    time_taken_this_frame = 0;

    while(running)
    {

        while(SDL_PollEvent(&event))
            On_Event(&event);

        On_Loop();
        On_Render();
        Do_Process_Clean();

        frames_rendered++;
        
        Wait_till_next_frame();
        
    }
 
    On_Cleanup();
 
    return 0;

}



void Main_App::Do_Process_Clean()
{
    vector<Process*>::iterator it2;
    for(std::vector<Process*>::iterator it = Process::Processes_to_kill.begin(); it != Process::Processes_to_kill.end(); ++it)
    {
        it2 = std::find(Process::Process_List.begin(), Process::Process_List.end(), *it);
        if(it2 != Process::Process_List.end())
            Process::Process_List.erase(it2);
        //delete *it2;
        //*it2 = NULL;
    }
    Process::Processes_to_kill.clear();
}


void Main_App::Quit()
{
    this -> running = False;
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

    time_taken_this_frame += SDL_GetTicks() - delay_ticks;

    if(time_taken_this_frame > 1000)
    {
        if(frames_rendered < desired_fps)
            current_fps = frames_rendered;
        else
            current_fps = desired_fps;
        frames_rendered = 0;
        time_taken_this_frame = 0;
    }

    if((SDL_GetTicks() - delay_ticks) < 1000 / desired_fps)
        SDL_Delay((1000 / desired_fps) - (SDL_GetTicks() - delay_ticks));

    delay_ticks = SDL_GetTicks();

}



int main(int argc, char* argv[])
{

    Main_App app;
    return app.On_Execute();

}

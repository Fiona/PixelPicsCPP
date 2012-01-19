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


map <string, Main_App::FuncGetter> Main_App::draw_strategies;


bool dir_exists(const char* path)
{
    if(path == NULL)
        return false;

    bool exists = false;

    DIR* dir = opendir(path);

    if(dir != NULL)
    {
        exists = True;    
        (void)closedir(dir);
    }

    return exists;
}


Main_App::Main_App()
{

    surf_display = NULL;
    running = True;
    desired_fps = 60;
    delay_ticks = 0;
    current_fps = 0;
    process_count = 0;
    frames_rendered = 0;
    python_interface = NULL;
    mouse = NULL;

    // Get the application data path depending on system
#if __LINUX__
    path_application_data = getenv("HOME");
    path_application_data += "/.pixelpics";
#elif __APPLE__
    path_application_data = getenv("HOME");
    path_application_data += "/Library/Application Support";
    path_application_data += "/PixelPics";
#elif __WIN32
    TCHAR path[MAX_PATH];
    if(SUCCEEDED(SHGetFolderPath(NULL, CSIDL_COMMON_APPDATA, NULL, 0, path)))
        path_application_data = path;
    path_application_data += "\StompyBlondie";

    if(!dir_exists(path_application_data.c_str()))
        mkdir(path_application_data.c_str(), 0777);

    path_application_data += "\PixelPics";
#endif

    if(!dir_exists(path_application_data.c_str()))
        mkdir(path_application_data.c_str(), 0777);

}

 
int Main_App::On_Execute()
{

	Py_NoSiteFlag = 1;
    Py_Initialize();

    if(On_Init() == False)
        return -1;
 
    SDL_Event event;

    desired_fps = 60;
    frames_rendered = 0;
    current_fps = 0;
    time_taken_this_frame = 0;

    while(running)
    {

        // Reset mouse states for these
        mouse->left_up = False;
        mouse->right_up = False;
        mouse->middle_up = False;
        mouse->x_rel = 0.0f;
        mouse->y_rel = 0.0f;
        mouse->wheel_up = False;
        mouse->wheel_down = False;

        while(SDL_PollEvent(&event))
            On_Event(&event);

        On_Loop();
        Do_Process_Clean();
        On_Render();

        frames_rendered++;
        process_count = Process::Process_List.size();
        
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

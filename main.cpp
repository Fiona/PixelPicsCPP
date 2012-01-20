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

    if(!boost::filesystem::exists(path_application_data.c_str()) || !boost::filesystem::is_directory(path_application_data.c_str()))
        boost::filesystem::create_directory(path_application_data.c_str());

    path_application_data += "\PixelPics";
#endif

    if(!boost::filesystem::exists(path_application_data.c_str()) || !boost::filesystem::is_directory(path_application_data.c_str()))
        boost::filesystem::create_directory(path_application_data.c_str());

    // Deal with loading default settings etc
    path_settings_file = path_application_data + FILE_SETTINGS;
    settings = new Settings(path_settings_file);

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


Settings::Settings(){ }

Settings::Settings(string _filename)
{

    filename = _filename;

    using boost::property_tree::ptree;
    ptree pt;

    try
    {
        read_json(filename, pt);
    }
    catch(std::exception &e)
    {
        pt.put("screen_width", DEFAULT_SETTING_SCREEN_WIDTH);
        pt.put("screen_height", DEFAULT_SETTING_SCREEN_HEIGHT);
        pt.put("full_screen", DEFAULT_SETTING_FULL_SCREEN);
    }

    screen_width = pt.get<float>("screen_width");
    screen_height = pt.get<float>("screen_height");
    full_screen = pt.get<bool>("full_screen");

}


bool Settings::save()
{

    using boost::property_tree::ptree;
    ptree pt;
    pt.put("screen_width", screen_width);
    pt.put("screen_height", screen_height);
    pt.put("full_screen", full_screen);
    try
    {
        write_json(filename, pt);
        return True;
    }
    catch(std::exception &e)
    {
        return False;
    }

}


int main(int argc, char* argv[])
{

    Main_App app;
    return app.On_Execute();

}

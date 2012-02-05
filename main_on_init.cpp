/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app initialisation
 ****************************/

#include <iostream>
using namespace std;
#include "main.h"


 
bool Main_App::On_Init()
{

    // Initialise SDL
    if(SDL_Init(SDL_INIT_EVERYTHING) < 0)
        return False;
    if(TTF_Init() < 0)
        return False;

    SDL_ShowCursor(SDL_DISABLE);

    // create window
    //SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
    //SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 2);
    Uint32 flags = SDL_HWSURFACE | SDL_GL_DOUBLEBUFFER | SDL_OPENGL;

    if(settings->full_screen)
        flags |= SDL_FULLSCREEN;

    surf_display = SDL_SetVideoMode(settings->screen_width, settings->screen_height, 32, flags);

    if(surf_display == NULL)
        return False;

    // set up opengl context
    glClearColor(0, 0, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT);

    glViewport(0, 0, settings->screen_width, settings->screen_height);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glOrtho(0, settings->screen_width, settings->screen_height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);

    glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    //glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    //glEnable(GL_LINE_SMOOTH);

    // Need this little titbit
    Process::default_texture_coords[0] = 1.0f;
    Process::default_texture_coords[1] = 1.0f;
    Process::default_texture_coords[3] = 1.0f;
    Process::default_texture_coords[4] = 1.0f;

    // Create the mouse
    mouse = new Mouse();

    // Load all the media
    Main_App::media = new Media();

    // Start up python
    python_interface = new Python_Interface(this);
    if(!python_interface -> initialise_python_interpreter())
        return False;

    // Set up process draw strategies
    draw_strategies["primitive_square"] = &Process::Draw_strategy_primitive_square;
    draw_strategies["gui_button"] = &Process::Draw_strategy_gui_button;
    draw_strategies["gui_window_frame"] = &Process::Draw_strategy_gui_window_frame;
    draw_strategies["puzzle"] = &Process::Draw_strategy_puzzle;
    draw_strategies["puzzle_pixel_message"] = &Process::Draw_strategy_puzzle_pixel_message;
    return True;

}


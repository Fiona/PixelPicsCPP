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

    // create window
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 2);
    surf_display = SDL_SetVideoMode(640, 480, 32, SDL_HWSURFACE | SDL_GL_DOUBLEBUFFER | SDL_OPENGL);

    if(surf_display == NULL)
        return False;

    // set up opengl context
    glClearColor(0, 0, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT);

    glViewport(0, 0, 640, 480);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glOrtho(0, 640, 480, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);

    glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_LINE_SMOOTH);

    // Need this little titbit
    default_texture_coords[0] = 1.0f;
    default_texture_coords[1] = 1.0f;
    default_texture_coords[3] = 1.0f;
    default_texture_coords[4] = 1.0f;

    // Start up python
    python_interface = new Python_Interface(this);
    if(!python_interface -> initialise_python_interpreter())
        return False;

    // Set up process draw strategies
    Process::Initialise_draw_strategies();
    draw_strategies["primitive_square"] = &Process::Draw_strategy_primitive_square;

    // Init game
    media = new Media();
    //new Main_input(this);

    return True;

}


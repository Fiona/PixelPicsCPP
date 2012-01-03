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

    surf_display = SDL_SetVideoMode(640, 480, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);

    if(surf_display == NULL)
        return False;

    media = new Media();

    new Main_input(this);

    return True;

}

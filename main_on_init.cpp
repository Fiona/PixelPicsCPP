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
 
    surf_display = SDL_SetVideoMode(640, 480, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);

    if(surf_display == NULL)
        return False;

    media = new Media();
    // Create game object
    new Ship(this, 300.0, 200.0);

/*
    new Ship(30.0, 20.0);
    new Ship(400.0, 200.0);
    new Ship(100.0, 150.0);
*/
    return True;

}

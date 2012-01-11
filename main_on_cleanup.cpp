/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Hoover file
 ****************************/

#include "main.h"
 
void Main_App::On_Cleanup()
{

    // Bye Bye SDL
    SDL_Quit();

    // Stop python
    Py_Finalize();

    // Kill all the loaded media items
    delete media;

}

/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app Header
 ****************************/

#ifndef _MAIN_H_
#define _MAIN_H_

#include <vector>

#include <GL/gl.h>
#include <SDL/SDL.h>
#include "media.h"
#include "process.h"
#include "image.h"
#include "game_objects.h"

// Yeah so what?
#define True true
#define False false


/*
 */
class Main_App
{
 
private:
    bool running;
    SDL_Surface*    surf_display;

public:
    Media* media;

    Main_App();

    int On_Execute();

    bool On_Init();
    
    void On_Event(SDL_Event* Event);
    
    void On_Loop();
    
    void On_Render();
    
    void On_Cleanup(); 

};


#endif

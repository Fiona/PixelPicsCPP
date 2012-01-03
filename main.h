/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app Header
 ****************************/

#ifndef _MAIN_H_
#define _MAIN_H_

#include <vector>
#include "boost/tuple/tuple.hpp"
#include "boost/format.hpp"

#include <GL/gl.h>
#include <SDL/SDL.h>
#include <SDL/SDL_timer.h>
#include <SDL/SDL_ttf.h>
#include "image.h"
#include "font.h"
#include "process.h"
#include "media.h"
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
    SDL_Surface* surf_display;
    int desired_fps;
    int delay_ticks;
    int frames_rendered;
    int time_taken_this_frame;

    void Wait_till_next_frame();

public:
    Media* media;
    std::vector<SDLKey> Keyboard_keys_down;
    int current_fps;

    Main_App();
    void Quit();
    int On_Execute();
    bool On_Init();   
    void On_Event(SDL_Event* Event);    
    void On_Loop();    
    void On_Render();    
    void Do_Process_Clean();
    void On_Cleanup(); 
    bool Keyboard_key_down(SDLKey Key);

};


#endif

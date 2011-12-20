/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Processesss
 ****************************/


#ifndef _PROCESS_H_
#define _PROCESS_H_

#include <vector>
#include <SDL/SDL.h>

#include "image.h"


/*
 */
class Process
{

public:
    static std::vector<Process*> Process_List;
    
public:
    float   x;
    float   y;
    Image*  image;
 
public:
    Process();
    virtual ~Process();
    virtual void Execute();
    virtual void Draw(SDL_Surface* screen);
    
};


#endif 

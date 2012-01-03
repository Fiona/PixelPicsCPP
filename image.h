/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Surface/Image loading header
 ****************************/

#ifndef _IMAGE_H_
#define _IMAGE_H_
 
#include <string>
using namespace std;

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

/*
 */ 
class Image
{

public:
    SDL_Surface* surface;

    Image();
    Image(string image);
    ~Image();

    int width;
    int height;
};
 
#endif

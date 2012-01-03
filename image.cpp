/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Surface/Image loading 
 ****************************/


#include <string>
#include "image.h"
using namespace std;


Image::Image()
{
    surface = NULL;
    width = 0;
    height = 0;
}

 
Image::Image(string image)
{

    surface = NULL;

    SDL_Surface* raw_surface = IMG_Load(image.c_str());
 
    if(raw_surface == NULL)
        return;

    surface = SDL_DisplayFormatAlpha(raw_surface);

    width = surface -> w;
    height = surface -> h;

    SDL_FreeSurface(raw_surface);

}


Image::~Image()
{

    if(surface != NULL)
    {
        SDL_FreeSurface(surface);
        surface = NULL;
    }

}

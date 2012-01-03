/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Surface/Image loading 
 ****************************/


#include <string>
#include <iostream>
#include "main.h"
using namespace std;


Image::Image()
{
    texture = 0;
    width = 0;
    height = 0;
}

 
Image::Image(string image)
{

    texture = 0;

    // Load the image in as an SDL surface and extract size info 
    SDL_Surface* raw_surface = IMG_Load(image.c_str());
 
    if(raw_surface == NULL)
        return;

    raw_surface = SDL_DisplayFormatAlpha(raw_surface);

    from_sdl_surface(raw_surface);

}



Image::Image(SDL_Surface *existing_surface)
{
    from_sdl_surface(existing_surface);
}


void Image::from_sdl_surface(SDL_Surface* raw_surface)
{

    width = raw_surface->w;
    height = raw_surface->h;

    // create GL texture from string representation of surface
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height,
                 0, GL_BGRA, GL_UNSIGNED_BYTE, raw_surface->pixels);

    SDL_FreeSurface(raw_surface);

    // create vertex list
    for(uint x = 0; x < 12; x++)
        vertex_list[x] = 0.0f;
    vertex_list[0] = width;
    vertex_list[1] = height;
    vertex_list[4] = height;
    vertex_list[6] = width;

}


Image::~Image()
{
    /*
    if(texture > 0)
    {
        glDeleteTextures(1, &texture);
        texture = 0;
    }
    */
}

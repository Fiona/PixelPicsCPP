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

#include <GL/gl.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

/*
 */ 
class Image
{

public:
    GLuint texture;

    Image();
    Image(string image);
    Image(SDL_Surface *existing_surface);
    ~Image();

    int width;
    int height;

    float vertex_list[12];

private:
    void from_sdl_surface(SDL_Surface* raw_surface);

};
 
#endif

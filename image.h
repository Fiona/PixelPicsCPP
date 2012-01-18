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
    Image();
    Image(string image, int _num_of_frames = 1);
    Image(SDL_Surface *existing_surface);
    ~Image();

    int width;
    int height;
    int num_of_frames;
    int surface_width;
    float sequence_pos;

    GLuint texture;
    float vertex_list[12];
    vector<float> get_tex_coord_list(int sequence);

private:
    void from_sdl_surface(SDL_Surface* raw_surface);

};
 
#endif

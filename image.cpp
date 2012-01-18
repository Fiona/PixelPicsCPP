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

 
Image::Image(string image, int _num_of_frames)
{

    texture = 0;

    // Load the image in as an SDL surface and extract size info 
    SDL_Surface* raw_surface = IMG_Load(image.c_str());
 
    if(raw_surface == NULL)
        return;

    raw_surface = SDL_DisplayFormatAlpha(raw_surface);

    from_sdl_surface(raw_surface);

    SDL_FreeSurface(raw_surface);

    num_of_frames = _num_of_frames;
    surface_width = width;
    if(num_of_frames > 1)
    {
        width = width / num_of_frames;
        sequence_pos = 0.01f * (((float)width / (float)surface_width) * 100.0f);
    }
    else
        sequence_pos = 0.0f;

    // create vertex list
    for(int x = 0; x < 12; x++)
        vertex_list[x] = 0.0f;
    vertex_list[0] = (float)width;
    vertex_list[1] = (float)height;
    vertex_list[4] = (float)height;
    vertex_list[6] = (float)width;

}



Image::Image(SDL_Surface *existing_surface)
{
    from_sdl_surface(existing_surface);
    num_of_frames = 1;

    // create vertex list
    for(int x = 0; x < 12; x++)
        vertex_list[x] = 0.0f;
    vertex_list[0] = (float)width;
    vertex_list[1] = (float)height;
    vertex_list[4] = (float)height;
    vertex_list[6] = (float)width;

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

}


vector<float> Image::get_tex_coord_list(int sequence)
{
    
    vector<float> t_list(8);

    float texture_x_from = (((float)width * (sequence - 1)) / (float)surface_width);
    float texture_x_to = (((float)width * sequence) / (float)surface_width);

    t_list[0] = texture_x_from; t_list[1] = 0.0;
    t_list[2] = texture_x_to; t_list[3] = 0.0;
    t_list[4] = texture_x_from; t_list[5] = 1.0;
    t_list[6] = texture_x_to; t_list[7] = 1.0;
/*
    t_list[0] = 0.0; t_list[1] = 0.0;
    t_list[2] = 0.5; t_list[3] = 0.0;
    t_list[4] = 0.0; t_list[5] = 1.0;
    t_list[6] = 0.5; t_list[7] = 1.0;

 */
    return t_list;

}


Image::~Image()
{

    if(texture > 0)
    {
        glDeleteTextures(1, &texture);
        texture = 0;
    }

}

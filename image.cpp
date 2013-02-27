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

 
Image::Image(string image, bool _for_repeat, int _num_of_frames)
{

    texture = 0;
    for_repeat = _for_repeat;

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

    make_vertex_list();
    make_texture_coords();

}


Image::Image(SDL_Surface *existing_surface, bool mipmaps)
{

    for_repeat = False;
    from_sdl_surface(existing_surface, mipmaps);
    num_of_frames = 1;
    make_vertex_list();
    make_texture_coords();

}


void Image::make_texture_coords()
{

    float texture_x_from;
    float texture_x_to;

    texture_coords = vector< vector<float> >(num_of_frames, vector<float>(8, 0.0f));

    for(int frame = 0; frame < num_of_frames; frame++)
    {

        if(num_of_frames == 1)
        {
            texture_x_from = 0.0f;
            texture_x_to = 1.0;
        }
        else
        {
            texture_x_from = sequence_pos*frame;
            texture_x_to = (sequence_pos*frame) + sequence_pos;
        }

        texture_coords[frame][0] = texture_x_to; texture_coords[frame][1] = 1.0f;
        texture_coords[frame][2] = texture_x_from; texture_coords[frame][3] = 1.0f;
        texture_coords[frame][4] = texture_x_to;
        texture_coords[frame][6] = texture_x_from;

    }

}


void Image::make_vertex_list()
{

    for(int x = 0; x < 12; x++)
        vertex_list[x] = 0.0f;
    vertex_list[0] = (float)width;
    vertex_list[1] = (float)height;
    vertex_list[4] = (float)height;
    vertex_list[6] = (float)width; 

}


void Image::from_sdl_surface(SDL_Surface* raw_surface, bool mipmaps)
{

    width = raw_surface->w;
    height = raw_surface->h;

    GLenum texture_format;
    GLint  nOfColors;

    nOfColors = raw_surface->format->BytesPerPixel;
    if(nOfColors == 4)
    {
        if(raw_surface->format->Rmask == 0x000000ff)
            texture_format = GL_RGBA;
        else
            texture_format = GL_BGRA;
    }
    else if(nOfColors == 3)
    {
        if(raw_surface->format->Rmask == 0x000000ff)
            texture_format = GL_RGB;
        else
            texture_format = GL_BGR;
    }
    else
    {
        cout << "warning: image is not truecolor" << endl;
        texture_format = GL_BGRA;
    }

    // create GL texture from string representation of surface
    texture = 0;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    if(for_repeat)
    {
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    }
    else
    {
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
    }

    if(mipmaps)
    {
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, width, height, texture_format, GL_UNSIGNED_BYTE, raw_surface->pixels);
    }
    else
    {
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height,
                     0, texture_format, GL_UNSIGNED_BYTE, raw_surface->pixels);
    }

}


Image::~Image()
{

    if(texture > 0)
    {
        glDeleteTextures(1, &texture);
        texture = 0;
    }

}

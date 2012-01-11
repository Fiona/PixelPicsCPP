/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Processesss source file
 ****************************/


#include "main.h"
#include <iostream>
#include <math.h>

std::vector<Process*> Process::Process_List;
std::vector<Process*> Process::Processes_to_kill;
boost::python::list Process::internal_list;

bool Process::z_order_dirty;
GLuint Process::current_bound_texture = -1;


 
Process::Process()
{
    x = y = 0.0f;
    z = 0;
    image = NULL;
    Process::z_order_dirty = True;
    Process::Process_List.push_back(this);
}


Process::~Process()
{
}


void Process::Init()
{
}


void Process::Execute()
{
}


void Process::Draw()
{

    if(image == NULL)
        return;

    glPushMatrix();

    // Get drawing coords
    tuple<float, float> draw_pos = get_screen_draw_position();

    // move to position
    glTranslatef(draw_pos.get<0>(), draw_pos.get<1>(), 0.0);

    // draw the triangle strip
    if(Process::current_bound_texture != image->texture)
    {
        glBindTexture(GL_TEXTURE_2D, image->texture);
        glVertexPointer(3, GL_FLOAT, 0, image->vertex_list);
        Process::current_bound_texture = image->texture;
    }

    glColor4f(1.0f, 1.0f, 1.0f, 1.0f);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    glPopMatrix();

}


void Process::Kill()
{
    Process::Processes_to_kill.push_back(this);
}


void Process::move_forward(float distance_to_travel, int rotation_to_move_in)
{
    x = x + distance_to_travel * cos(deg_to_rad(rotation_to_move_in));
    y = y + distance_to_travel * sin(deg_to_rad(rotation_to_move_in));
}


float Process::deg_to_rad(float deg)
{
    return (3.1415926f / 180.0f) * deg;
}
 

float Process::rad_to_deg(float rad)
{
    return rad * 180.0f / 3.1415926f;
}


tuple<float, float> Process::get_screen_draw_position()
{

    if(image == NULL)
        return tuple<float, float>(x, y);

    return tuple<float, float>(x - (image -> width / 2), y - (image -> height / 2));

}


/*
 *
 */
void ProcessWrapper::Init(){ }
void ProcessWrapper::Init_default()
{
    this->Process::Init();
}


void ProcessWrapper::Execute()
{
    if(!has_init)
    {
        boost::python::call_method<void>(self, "Init");    
        has_init = True;
    }
    boost::python::call_method<void>(self, "Execute");
}
void ProcessWrapper::Execute_default()
{
    this->Process::Execute();
}


ProcessWrapper::ProcessWrapper(PyObject* _self) : Process()
{
    has_init = False;
    self = _self;
    Process::internal_list.append(
        boost::python::object(boost::python::handle<>(boost::python::borrowed(self)))
        );
}



/*
 *
 */
Text::Text(): Process()
{
    font = NULL;
    alignment = 0;
    text_width = 0;
    text_height = 0;
    text = "";
}

Text::Text(Font* _font, float _x, float _y, int _alignment, string _text): Process()
{
    font = _font;
    x = _x;
    y = _y;
    z = Z_TEXT;
    alignment = _alignment;
    text_width = 0;
    text_height = 0;

    set_text(_text);

}


Text::~Text()
{
/*
    if(image != NULL)
        delete image;
    image = NULL;
*/
}


void Text::set_text(string new_text)
{

    text = new_text;
    generate_new_text_image();

}


void Text::generate_new_text_image()
{

    if(image != NULL)
        delete image;

    if(font == NULL || text == "")
        return;

    // Create a new SDL texture to put our image in.
    SDL_Color colour = {255, 255, 255};
    SDL_Surface *text_surface = TTF_RenderText_Blended(font->font, text.c_str(), colour);

    // We need to work out the nearest power of 2 so
    // the texture we generate is valid
    int width = text_surface->w;
    int height = text_surface->h;

    text_width = width;
    text_height = height;
                       
    int h = 16;
    while(h < height)
        h = h * 2;
    int w = 16;
    while(w < width)
        w = w * 2;

    SDL_Surface *final_surface;

    final_surface = text_surface;
    final_surface->refcount++;

    image = new Image(final_surface);

    SDL_FreeSurface(text_surface);
    SDL_FreeSurface(final_surface);

}



tuple<float, float> Text::get_screen_draw_position()
{

    switch(alignment)
    {
    case TEXT_ALIGN_TOP:
        return tuple<float, float>(x - (text_width / 2), y);
    case TEXT_ALIGN_TOP_RIGHT:
        return tuple<float, float>(x - text_width, y);
    case TEXT_ALIGN_CENTER_LEFT:
        return tuple<float, float>(x, y - (text_height / 2));
    case TEXT_ALIGN_CENTER:
        return tuple<float, float>(x - (text_width / 2), y - (text_height / 2));
    case TEXT_ALIGN_CENTER_RIGHT:
        return tuple<float, float>(x - text_width, y - (text_height / 2));
    case TEXT_ALIGN_BOTTOM_LEFT:
        return tuple<float, float>(x, y - text_height);
    case TEXT_ALIGN_BOTTOM:
        return tuple<float, float>(x - (text_width / 2), y - text_height);
    case TEXT_ALIGN_BOTTOM_RIGHT:
        return tuple<float, float>(x - text_width, y - text_height);
    default:
        return tuple<float, float>(x, y);
    }

}


/*
 *
 */
void TextWrapper::Execute(){}
void TextWrapper::Execute_default()
{
    this->Text::Execute();
}


TextWrapper::TextWrapper(PyObject* _self, Font* _font, float _x, float _y, int _alignment, string _text) : Text(_font, _x, _y, _alignment, _text)
{
    self = _self;
    Process::internal_list.append(
        boost::python::object(boost::python::handle<>(boost::python::borrowed(self)))
        );
}

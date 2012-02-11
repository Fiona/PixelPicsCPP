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

vector<float> Process::default_texture_coords(8);

bool Process::z_order_dirty;
GLuint Process::current_bound_texture = -1;


 
Process::Process()
{
    x = y = 0.0f;
    z = 0;
    scale = 1.0;
    rotation = 0;
    colour.resize(3, 1.0f);
    scale_pos.resize(2, 0.0f);
    clip.resize(4, 0.0f);
    alpha = 1.0;
    image_sequence = 1;
    draw_strategy = "";
    is_dead = False;

    self = NULL;

    image = NULL;
    Process::z_order_dirty = True;
    Process::Process_List.push_back(this);
}


Process::~Process()
{
}


void Process::Execute()
{
}


void Process::On_Exit()
{
}


void Process::Draw()
{

    if(image == NULL || is_dead == True)
        return;

    glPushMatrix();

    // Get drawing coords
    tuple<float, float> draw_pos = get_screen_draw_position();

    // Clip the process if necessary
    // glScissor assumes origin as bottom-left rather than top-left which explains the fudging with the second param
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    // glrotate works by you translating to the point around which you wish to rotate
    // and applying the rotation you can translate back to apply the real translation
    // position
    if(rotation < 0 || rotation > 0)
    {
        float rot_x = (draw_pos.get<0>() * scale) + ((image->width/2) * scale);
        float rot_y = (draw_pos.get<1>() * scale) + ((image->height/2) * scale);
        glTranslatef(rot_x, rot_y, 0.0f);
        glRotatef((float)rotation, 0.0f, 0.0f, 1.0f);
        glTranslatef(-rot_x, -rot_y, 0.0f);
    }

    // move to position
    glTranslatef(draw_pos.get<0>(), draw_pos.get<1>(), 0.0f);

    // scaling
    if(scale < 1.0f || scale > 1.0f)
    {
        glTranslatef(scale_pos[0], scale_pos[1], 0.0f);
        glScalef(scale, scale, 1.0f);
        glTranslatef(-scale_pos[0], -scale_pos[1], 0.0f);
    }

    // Text texture coords to different ones for texture atlasses
    if(image->num_of_frames > 1)
        glTexCoordPointer(2, GL_FLOAT, 0, &image->texture_coords[image_sequence-1][0]);
                               
    // Binding texture
    if(Process::current_bound_texture != image->texture)
    {
        glBindTexture(GL_TEXTURE_2D, image->texture);
        glVertexPointer(3, GL_FLOAT, 0, image->vertex_list);
        Process::current_bound_texture = image->texture;
    }

    // Changing colour and transparency
    glColor4f(colour[0], colour[1], colour[2], alpha);

    // draw the triangle strip
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    // Reset the texture coords back to default if necessary
    if(image->num_of_frames > 1)
        glTexCoordPointer(2, GL_FLOAT, 0, &Process::default_texture_coords[0]);

    // Stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

    glPopMatrix();

}


void Process::Kill()
{
    if(is_dead)
        return;
    Process::Processes_to_kill.push_back(this);
    is_dead = True;
}


void Process::Set_z(int new_z)
{
    z = new_z;
    Process::z_order_dirty = True;
}


void Process::Set_colour(boost::python::object list)
{
    colour[0] = boost::python::extract<float>(list[0]);
    colour[1] = boost::python::extract<float>(list[1]);
    colour[2] = boost::python::extract<float>(list[2]);
}


void Process::Set_clip(boost::python::object list)
{
    clip[0] = boost::python::extract<float>(list[0]);
    clip[1] = boost::python::extract<float>(list[1]);
    clip[2] = boost::python::extract<float>(list[2]);
    clip[3] = boost::python::extract<float>(list[3]);
}


void Process::Set_scale_pos(boost::python::object list)
{
    scale_pos[0] = boost::python::extract<float>(list[0]);
    scale_pos[1] = boost::python::extract<float>(list[1]);
}


void Process::move_forward(float distance_to_travel, int rotation_to_move_in)
{
    x = x + distance_to_travel * cos(deg_to_rad((float)rotation_to_move_in));
    y = y + distance_to_travel * sin(deg_to_rad((float)rotation_to_move_in));
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
 * DRAW STRATEGIES
 */
void Process::Draw_strategy_gui_button()
{

    if(alpha <= 0.0)
        return;

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    // Draw the background gradient
    glPushMatrix();
    glEnable(GL_TEXTURE_2D);

    glTexCoordPointer(2, GL_FLOAT, 0, &image->texture_coords[image_sequence-1][0]);
                               
    glBindTexture(GL_TEXTURE_2D, image->texture);
    Process::current_bound_texture = image->texture;

    float vertex_list[12];
    for(int i = 0; i < 12; i++)
        vertex_list[i] = 0.0f;
    vertex_list[0] = (float)width;
    vertex_list[1] = (float)height;
    vertex_list[4] = (float)height;
    vertex_list[6] = (float)width; 

    glVertexPointer(3, GL_FLOAT, 0, vertex_list);

    glTranslatef(x, y, 0.0);
    glColor4f(1.0, 1.0, 1.0, alpha);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    glTexCoordPointer(2, GL_FLOAT, 0, &Process::default_texture_coords[0]);

    // Draw the surrounding rectangle    
    glDisable(GL_TEXTURE_2D);
    glLineWidth(2.0);
    glColor4f(.5, .5, .5, alpha);
    glBegin(GL_LINE_LOOP);
    glVertex2f(0.0, 0.0);
    glVertex2f(width, 0.0);
    glVertex2f(width, height);
    glVertex2f(0.0, height);
    glEnd();
    glEnable(GL_TEXTURE_2D);

    glPopMatrix();

    // Stop clip
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

}


void Process::Draw_strategy_gui_window_frame()
{

    if(alpha <= 0.0)
        return;

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));
    tuple<float, float> draw_pos = get_screen_draw_position();
    float draw_x = draw_pos.get<0>();
    float draw_y = draw_pos.get<1>();

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    glPushMatrix();

    glDisable(GL_TEXTURE_2D);

    // Background grey shadow
    glColor4f(0.7, 0.7, 0.7, 0.7);
    glBegin(GL_QUADS);
    glVertex2f(draw_x + 12.0f,        draw_y + 12.0f);
    glVertex2f(draw_x + width - 4.0f, draw_y + 12.0f);
    glVertex2f(draw_x + width - 4.0f, draw_y + height - 4.0f);
    glVertex2f(draw_x + 12.0f,        draw_y + height - 4.0f);
    glEnd();

    // Background of frame
    glBegin(GL_QUADS);
    glColor4f(0.8, 1.0, 1.0, 1.0);
    glVertex2f(draw_x + 8.0f,          draw_y + 8.0f);
    glVertex2f(draw_x + width - 8.0f,  draw_y + 8.0f);
    glColor4f(1.0, 1.0, 1.0, 1.0);
    glVertex2f(draw_x + width - 8.0f,  draw_y + height - 8.0f);
    glVertex2f(draw_x + 8.0f,          draw_y + height - 8.0f);
    glEnd();

    // Frame border
    glColor4f(0.7, 0.7, 0.7, 1.0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(draw_x + 10.0f,          draw_y + 10.0f);
    glVertex2f(draw_x + width - 10.0f,  draw_y + 10.0f);
    glVertex2f(draw_x + width - 10.0f,  draw_y + height - 10.0f);
    glVertex2f(draw_x + 10.0f,          draw_y + height - 10.0f);
    glEnd();

    // Title shadow
    glColor4f(0.7, 0.7, 0.7, 0.7);
    glBegin(GL_QUADS);
    glVertex2f(draw_x + 16.0f,   draw_y + 6.0f);
    glVertex2f(draw_x + 250.0f,  draw_y + 6.0f);
    glVertex2f(draw_x + 250.0f,  draw_y + 20.0f);
    glVertex2f(draw_x + 16.0f,   draw_y + 20.0f);
    glEnd();

    // Title 
    glColor4f(1.0, 1.0, 1.0, 1.0);
    glBegin(GL_QUADS);
    glVertex2f(draw_x + 10.0f,   draw_y);
    glVertex2f(draw_x + 244.0f,  draw_y);
    glVertex2f(draw_x + 244.0f,  draw_y + 16.0f);
    glVertex2f(draw_x + 10.0f,   draw_y + 16.0f);
    glEnd();

    glEnable(GL_TEXTURE_2D);

    glPopMatrix();

    // Stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

}

void Process::Draw_strategy_gui_text_input()
{

    if(alpha <= 0.0)
        return;

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));
    bool active = boost::python::extract<float>(self_.attr("active"));
    tuple<float, float> draw_pos = get_screen_draw_position();
    float draw_x = draw_pos.get<0>();
    float draw_y = draw_pos.get<1>();

    glPushMatrix();

    glDisable(GL_TEXTURE_2D);

    glColor4f(0.0, 0.0, 0.0, 1.0);
    glBegin(GL_QUADS);
    glVertex2f(draw_x, draw_y);
    glVertex2f(width + draw_x, draw_y);
    glVertex2f(width + draw_x, height + draw_y);
    glVertex2f(draw_x, height + draw_y);
    glEnd();

    if(active)
        glColor4f(0.8, 0.8, 0.8, 1.0);
    else
        glColor4f(0.5, 0.5, 0.5, 1.0);
    glLineWidth(1.0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(draw_x, draw_y);
    glVertex2f(width + draw_x, draw_y);
    glVertex2f(width + draw_x, height + draw_y);
    glVertex2f(draw_x, height + draw_y);
    glEnd();

    glEnable(GL_TEXTURE_2D);

    glPopMatrix();

    // Stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

}


void Process::Draw_strategy_gui_dropdown_currently_selected()
{

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));

    glPushMatrix();

    glDisable(GL_TEXTURE_2D);

    glColor4f(0.0, 0.0, 0.0, 1.0);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(width + x, y);
    glVertex2f(width + x, height + y);
    glVertex2f(x, height + y);
    glEnd();

    glColor4f(0.5, 0.5, 0.5, 1.0);
    glLineWidth(1.0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(x, y);
    glVertex2f(width + x, y);
    glVertex2f(width + x, height + y);
    glVertex2f(x, height + y);
    glEnd();

    glEnable(GL_TEXTURE_2D);
    glColor4f(1.0, 1.0, 1.0, 1.0);
    glTranslatef(x + width - 25.0, y + 1.0, 0.0);
    glTexCoordPointer(2, GL_FLOAT, 0, &image->texture_coords[image_sequence-1][0]);
    glBindTexture(GL_TEXTURE_2D, image->texture);
    glVertexPointer(3, GL_FLOAT, 0, image->vertex_list);
    Process::current_bound_texture = image->texture;
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
    glTexCoordPointer(2, GL_FLOAT, 0, &Process::default_texture_coords[0]);

    glPopMatrix();

}


void Process::Draw_strategy_gui_dropdown_options()
{

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));
    int hovered_item = boost::python::extract<int>(self_.attr("hovered_item"));
    int display_height = boost::python::extract<int>(self_.attr("display_height"));
    int num_dropdown_options = boost::python::extract<int>(self_.attr("num_dropdown_options"));

    if(width == 0 || height == 0)
        return;

    glPushMatrix();
    glDisable(GL_TEXTURE_2D);

    // Background behind items
    glColor4f(0.0, 0.0, 0.0, 1.0);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(width + x, y);
    glVertex2f(width + x, height + y);
    glVertex2f(x, height + y);
    glEnd();

    // highlight on hovered item
    if(hovered_item > -1)
    {
        glColor4f(0.2, 0.2, 0.2, 1.0);
        glBegin(GL_QUADS);
        glVertex2f(x, y + (display_height * hovered_item));
        glVertex2f(width + x, y + (display_height * hovered_item));
        glVertex2f(width + x, y + (display_height * (hovered_item + 1)));
        glVertex2f(x, y + (display_height * (hovered_item + 1)));
        glEnd();
    }

    // Border around all items
    int start_y = 0;
    for(int i = 0; i < num_dropdown_options; i++)
    {
        glColor4f(0.4, 0.4, 0.4, 1.0);
        glLineWidth(1.0);
        glBegin(GL_LINE_LOOP);
        glVertex2f(x, y + start_y);
        glVertex2f(width + x, y + start_y);
        glVertex2f(width + x, y + start_y + display_height);
        glVertex2f(x, y + start_y + display_height);
        glEnd();
        start_y += display_height;
    }

    glEnable(GL_TEXTURE_2D);
    glPopMatrix();

}


void Process::Draw_strategy_gui_scroll_window()
{

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));

    if(width == 0 || height == 0)
        return;

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    glPushMatrix();
    glDisable(GL_TEXTURE_2D);

    //glVertex2f(top_left[0], top_left[1])
    //glVertex2f(bottom_right[0], top_left[1])
    //glVertex2f(bottom_right[0], bottom_right[1])
    //glVertex2f(top_left[0], bottom_right[1])

    glColor4f(0.5, 0.5, 0.5, 0.5);
    glBegin(GL_QUADS);
    glVertex2f(x, y);
    glVertex2f(width + x, y);
    glVertex2f(width + x, height + y);
    glVertex2f(x, height + y);
    glEnd();

    glColor4f(0.0, 0.0, 0.0, 1.0);
    glLineWidth(1.0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(x, y);
    glVertex2f(width + x, y);
    glVertex2f(width + x, height + y);
    glVertex2f(x, height + y);
    glEnd();

    glEnable(GL_TEXTURE_2D);
    glPopMatrix();

    // stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

}


void Process::Draw_strategy_primitive_square()
{
 
    float square_x = boost::python::extract<float>(self_.attr("primitive_square_x"));
    float square_y = boost::python::extract<float>(self_.attr("primitive_square_y"));
    float width = boost::python::extract<float>(self_.attr("primitive_square_width"));
    float height = boost::python::extract<float>(self_.attr("primitive_square_height"));
    boost::python::tuple colour = boost::python::extract<boost::python::tuple>(self_.attr("primitive_square_colour"))();

    bool filled;
    if(hasattr(self_, "primitive_square_filled"))
        filled = boost::python::extract<bool>(self_.attr("primitive_square_filled"));
    else
        filled = True;

    bool four_colours;
    if(hasattr(self_, "primitive_square_four_colours"))
        four_colours = boost::python::extract<bool>(self_.attr("primitive_square_four_colours"));
    else
        four_colours = False;

    glPushMatrix();

    glDisable(GL_TEXTURE_2D);

    if(filled)
        glBegin(GL_QUADS);
    else
    {

        float line_width;
        if(hasattr(self_, "primitive_square_line_width"))
            line_width = boost::python::extract<float>(self_.attr("primitive_square_line_width"));
        else
            line_width = 1.0;

        glLineWidth(line_width);
        glBegin(GL_LINE_LOOP);

    }

    boost::python::tuple col_1;
    if(four_colours)
        col_1 = boost::python::extract<boost::python::tuple>(colour[0]);
    else
        col_1 = colour;
    glColor4f(
        boost::python::extract<float>(col_1[0]),
        boost::python::extract<float>(col_1[1]),
        boost::python::extract<float>(col_1[2]),
        boost::python::extract<float>(col_1[3])
        );

    glVertex2f(square_x, square_y);

    if(four_colours)
    {
        col_1 = boost::python::extract<boost::python::tuple>(colour[1]);
        glColor4f(
            boost::python::extract<float>(col_1[0]),
            boost::python::extract<float>(col_1[1]),
            boost::python::extract<float>(col_1[2]),
            boost::python::extract<float>(col_1[3])
            );
    }

    glVertex2f(square_x + width, square_y);

    if(four_colours)
    {
        col_1 = boost::python::extract<boost::python::tuple>(colour[2]);
        glColor4f(
            boost::python::extract<float>(col_1[0]),
            boost::python::extract<float>(col_1[1]),
            boost::python::extract<float>(col_1[2]),
            boost::python::extract<float>(col_1[3])
            );
    }

    glVertex2f(square_x + width, square_y + height);

    if(four_colours)
    {
        col_1 = boost::python::extract<boost::python::tuple>(colour[3]);
        glColor4f(
            boost::python::extract<float>(col_1[0]),
            boost::python::extract<float>(col_1[1]),
            boost::python::extract<float>(col_1[2]),
            boost::python::extract<float>(col_1[3])
            );
    }

    glVertex2f(square_x, square_y + height);
    glEnd();
                                          
    glEnable(GL_TEXTURE_2D);

    glPopMatrix();

    bool call_parent;
    if(hasattr(self_, "draw_strategy_call_parent"))
        call_parent = boost::python::extract<bool>(self_.attr("draw_strategy_call_parent"));
    else
        call_parent = True;

    if(call_parent)
        this->Draw();

}


void Process::Draw_strategy_puzzle_pixel_message()
{

    float screen_width = boost::python::extract<float>(self_.attr("draw_strategy_screen_width"));
    int height = boost::python::extract<float>(self_.attr("height"));

    glPopMatrix();
    glDisable(GL_TEXTURE_2D);
    
    glBegin(GL_QUADS);
      glColor4f(0.6, 0.8, 0.8, 0.0);
      glVertex2f(0.0, y - (float)(height / 2));
      glColor4f(0.6, 0.8, 0.8, 0.0);
      glVertex2f(screen_width, y - (float)(height / 2));
      glColor4f(0.6, 0.8, 0.8, alpha);
      glVertex2f(screen_width, y + (float)(height / 2));
      glColor4f(0.6, 0.8, 0.8, alpha);
      glVertex2f(0.0, y + (float)(height / 2));
    glEnd();

    glBegin(GL_QUADS);
      glColor4f(0.6, 0.8, 0.8, alpha);
      glVertex2f(0.0, y + (float)(height / 2));
      glColor4f(0.6, 0.8, 0.8, alpha);
      glVertex2f(screen_width, y + (float)(height / 2));
      glColor4f(0.6, 0.8, 0.8, 0.0);
      glVertex2f(screen_width, y + (float)(height / 2) + (float)height);
      glColor4f(0.6, 0.8, 0.8, 0.0);
      glVertex2f(0.0, y + (float)(height / 2) + (float)height);
    glEnd();

    glEnable(GL_TEXTURE_2D);
    glPushMatrix();

}


void Process::Draw_strategy_puzzle()
{

    // ****************
    // Get prelim vals from python
    // ****************
    float screen_width;
    float screen_height;
    float camera_x;
    float camera_y;
    float zoom_level;
    int grid_x;
    int grid_y;
    float grid_width;
    float grid_height;
    int current_puzzle_width;
    int current_puzzle_height;
    int hovered_column;
    int hovered_row;
    boost::python::object game;
    boost::python::object core;
    Media* media;
    boost::python::list current_puzzle_state;

        try
        {

             screen_width = boost::python::extract<float>(self_.attr("draw_strategy_screen_width"));
             screen_height = boost::python::extract<float>(self_.attr("draw_strategy_screen_height"));
             camera_x = boost::python::extract<float>(self_.attr("draw_strategy_camera_x"));
             camera_y = boost::python::extract<float>(self_.attr("draw_strategy_camera_y"));
             zoom_level = boost::python::extract<float>(self_.attr("draw_strategy_current_zoom_level"));
             current_puzzle_width = boost::python::extract<float>(self_.attr("draw_strategy_current_puzzle_width"));
             current_puzzle_height = boost::python::extract<float>(self_.attr("draw_strategy_current_puzzle_height"));
             grid_x = boost::python::extract<int>(self_.attr("grid_x"));
             grid_y = boost::python::extract<int>(self_.attr("grid_y"));
             grid_width = boost::python::extract<float>(self_.attr("grid_width"));
             grid_height = boost::python::extract<float>(self_.attr("grid_height"));
             hovered_column = boost::python::extract<int>(self_.attr("hovered_column"));
             hovered_row = boost::python::extract<int>(self_.attr("hovered_row"));
             game = boost::python::extract<boost::python::object>(self_.attr("game"));
             core = boost::python::extract<boost::python::object>(game.attr("core"));
             media = boost::python::extract<Media*>(core.attr("media"));
             current_puzzle_state = boost::python::extract<boost::python::list>(self_.attr("draw_strategy_current_puzzle_state"));

        }
        catch(boost::python::error_already_set const &)
        {
            PyErr_Print();
        }

    // ****************
    // Set up matrix
    // ****************
    glPushMatrix();

    glTranslatef(
        ((grid_x - camera_x) * zoom_level) + (screen_width/2),
        ((grid_y - camera_y) * zoom_level) + (screen_height/2),
        0.0
        );

    glScalef(zoom_level, zoom_level, 1.0);

    // ****************
    // White puzzle background
    // ****************
    glDisable(GL_TEXTURE_2D);
    glColor4f(1.0, 1.0, 1.0, 0.9);
    glBegin(GL_QUADS);
    glVertex2f(0.0, 0.0);
    glVertex2f(grid_width, 0);
    glVertex2f(grid_width, grid_height);
    glVertex2f(0, grid_height);
    glEnd();

    // ****************
    // Textured background
    // ****************
    float coords_x = grid_width / (PUZZLE_CELL_WIDTH * 2);
    float coords_y = grid_height / (PUZZLE_CELL_HEIGHT * 2);
    float tex_coords_pointer[] = {coords_x, coords_y, 0.0, coords_y, coords_x, 0.0, 0.0, 0.0};
    glTexCoordPointer(2, GL_FLOAT, 0, tex_coords_pointer);
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, media->gfx["gui_puzzle_grid_background"]->texture);
    float vertex_pointer[] = {grid_width, grid_height, 0.0, 0.0, grid_height, 0.0, grid_width, 0.0, 0.0, 0.0, 0.0, 0.0};
    glVertexPointer(3, GL_FLOAT, 0, vertex_pointer);
    glColor4f(1.0, 1.0, 1.0, 1.0);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
     
    // ****************
    //Gradients behind numbers
    // ****************
    float draw_start;
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glEnableClientState(GL_COLOR_ARRAY);
    glDisable(GL_TEXTURE_2D);

    static vector<float> number_gradient_squares;
    if(number_gradient_squares.size() == 0)
    {

        draw_start = 0;
        for(int y = 0; y < current_puzzle_height; y++)
        {
            
            if(y % 2)
            {
                draw_start += PUZZLE_CELL_HEIGHT;
                continue;
            }

            number_gradient_squares.push_back(-PUZZLE_HINT_GRADIENT_WIDTH);
            number_gradient_squares.push_back(draw_start);

            number_gradient_squares.push_back(0.0);
            number_gradient_squares.push_back(draw_start);

            number_gradient_squares.push_back(0.0);
            number_gradient_squares.push_back(draw_start + PUZZLE_CELL_HEIGHT);

            number_gradient_squares.push_back(-PUZZLE_HINT_GRADIENT_WIDTH);
            number_gradient_squares.push_back(draw_start + PUZZLE_CELL_HEIGHT);

            draw_start += (float)PUZZLE_CELL_HEIGHT;

        }

        draw_start = 0;
        for(int x = 0; x < current_puzzle_width; x++)
        {
            
            if(x % 2)
            {
                draw_start += PUZZLE_CELL_WIDTH;
                continue;
            }

            number_gradient_squares.push_back(draw_start);
            number_gradient_squares.push_back(-PUZZLE_HINT_GRADIENT_WIDTH);

            number_gradient_squares.push_back(draw_start + PUZZLE_CELL_HEIGHT);
            number_gradient_squares.push_back(-PUZZLE_HINT_GRADIENT_WIDTH);

            number_gradient_squares.push_back(draw_start + PUZZLE_CELL_HEIGHT);
            number_gradient_squares.push_back(0.0);

            number_gradient_squares.push_back(draw_start);
            number_gradient_squares.push_back(0.0);

            draw_start += (float)PUZZLE_CELL_WIDTH;

        }

    }

    static vector<float> number_gradient_colours;
    if(number_gradient_colours.size() == 0)
    {

        float horisontal_colours[] = {
            1.0, 1.0, 1.0, 0.0,
            .5, .7, .8, 1.0,
            .5, .7, .8, 1.0,
            1.0, 1.0, 1.0, 0.0
        };

        float vertical_colours[] = {
            1.0, 1.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            .5, .7, .8, 1.0,
            .5, .7, .8, 1.0
        };

        for(int y = 0; y < current_puzzle_height; y++)
        {
            if(y % 2)
                continue;
            for(int i = 0; i < 16; i++)
                number_gradient_colours.push_back(horisontal_colours[i]);
        }

        for(int x = 0; x < current_puzzle_width; x++)
        {
            if(x % 2)
                continue;
            for(int i = 0; i < 16; i++)
                number_gradient_colours.push_back(vertical_colours[i]);
        }

    }

    glColorPointer(4, GL_FLOAT, 0, &number_gradient_colours[0]);
    glVertexPointer(2, GL_FLOAT, 0, &number_gradient_squares[0]);
    glDrawArrays(GL_QUADS, 0, number_gradient_squares.size() / 2);
    glDisableClientState(GL_COLOR_ARRAY);

    // ****************
    // Column / Row Hover
    // ****************
    if(hovered_row > -1)
    {
        glColor4f(.5, .5, 1.0, .2);
        glBegin(GL_QUADS);
        glVertex2f(0.0, (float)(PUZZLE_CELL_HEIGHT * hovered_row));
        glVertex2f(grid_width, (float)(PUZZLE_CELL_HEIGHT * hovered_row));
        glVertex2f(grid_width, (float)((PUZZLE_CELL_HEIGHT * hovered_row) + PUZZLE_CELL_HEIGHT));
        glVertex2f(0.0, (float)((PUZZLE_CELL_HEIGHT * hovered_row) + PUZZLE_CELL_HEIGHT));
        glEnd();
    }

    if(hovered_column > -1)
    {
        glColor4f(.5, .5, 1.0, .2);
        glBegin(GL_QUADS);
        glVertex2f((float)(PUZZLE_CELL_WIDTH * hovered_column), 0.0);
        glVertex2f((float)((PUZZLE_CELL_WIDTH * hovered_column) + PUZZLE_CELL_WIDTH), 0.0);
        glVertex2f((float)((PUZZLE_CELL_WIDTH * hovered_column) + PUZZLE_CELL_WIDTH), grid_height);
        glVertex2f((float)(PUZZLE_CELL_WIDTH * hovered_column), grid_height);
        glEnd();
    }

    // ****************
    // Grid Lines
    // ****************
    static vector<float> grid_lines;
    if(grid_lines.size() == 0)
    {

        draw_start = (float)PUZZLE_CELL_HEIGHT;
        for(int y = 0; y < current_puzzle_width; y++)
        {
            grid_lines.push_back(draw_start);
            grid_lines.push_back(0.0);
            grid_lines.push_back(draw_start);
            grid_lines.push_back(grid_height);
            draw_start += (float)PUZZLE_CELL_HEIGHT;
        } 

        draw_start = (float)PUZZLE_CELL_WIDTH;
        for(int x = 0; x < current_puzzle_height; x++)
        {
            grid_lines.push_back(0.0);
            grid_lines.push_back(draw_start);
            grid_lines.push_back(grid_width);
            grid_lines.push_back(draw_start);
            draw_start += (float)PUZZLE_CELL_WIDTH;
        } 

    }


    glLineWidth(1.0 / zoom_level);
    glColor4f(0.3, 0.3, 0.3, 1.0);
    glVertexPointer(2, GL_FLOAT, 0, &grid_lines[0]);
    glDrawArrays(GL_LINES, 0, (current_puzzle_width + current_puzzle_height) * 2);
    
    // ****************
    // Every five lines draw marker lines
    // ****************
    static vector<float> every_five_lines;
    if(every_five_lines.size() == 0)
    {

        draw_start = (float)(PUZZLE_CELL_HEIGHT * 5);
        for(int y = 0; y < (int)ceil((float)current_puzzle_width / 5) - 1; y++)
        {
            every_five_lines.push_back(draw_start);
            every_five_lines.push_back(0.0);
            every_five_lines.push_back(draw_start);
            every_five_lines.push_back(grid_height);
            draw_start += (float)(PUZZLE_CELL_HEIGHT * 5);
        } 

        draw_start = (float)(PUZZLE_CELL_WIDTH * 5);
        for(int x = 0; x < (int)ceil((float)current_puzzle_height / 5) - 1; x++)
        {
            every_five_lines.push_back(0.0);
            every_five_lines.push_back(draw_start);
            every_five_lines.push_back(grid_width);
            every_five_lines.push_back(draw_start);
            draw_start += (float)(PUZZLE_CELL_WIDTH * 5);
        } 

    }

    glLineWidth(2.0 / zoom_level);
    glColor4f(0.3, 0.7, 0.3, 1.0);
    glVertexPointer(2, GL_FLOAT, 0, &every_five_lines[0]);
    glDrawArrays(GL_LINES, 0, every_five_lines.size() / 2);

    // ****************
    // Puzzle border
    // ****************
    glColor4f(0.0, 0.0, 0.0, 1.0);
    glLineWidth(2.0 / zoom_level);
    glBegin(GL_LINE_LOOP);
    glVertex2f(0.0, 0.0);
    glVertex2f(grid_width, 0.0);
    glVertex2f(grid_width, grid_height);
    glVertex2f(0.0, grid_height);
    glEnd();

    // ****************
    // Cell Hover
    // ****************
    if(hovered_row > -1 && hovered_column > -1)
    {
        glColor4f(1.0, 0.0, 0.0, .8);
        glBegin(GL_LINE_LOOP);
        glLineWidth(3.0 / zoom_level);
        glVertex2f((float)(PUZZLE_CELL_WIDTH * hovered_column), (float)(PUZZLE_CELL_HEIGHT * hovered_row));
        glVertex2f((float)(PUZZLE_CELL_WIDTH + (PUZZLE_CELL_WIDTH * hovered_column)), (float)(PUZZLE_CELL_HEIGHT * hovered_row));
        glVertex2f((float)(PUZZLE_CELL_WIDTH + (PUZZLE_CELL_WIDTH * hovered_column)), (float)(PUZZLE_CELL_HEIGHT + (PUZZLE_CELL_HEIGHT * hovered_row)));
        glVertex2f((float)(PUZZLE_CELL_WIDTH * hovered_column), (float)(PUZZLE_CELL_HEIGHT + (PUZZLE_CELL_HEIGHT * hovered_row)));
        glEnd();
    }

    // ****************
    // Set up for drawing markers
    // ****************
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);
    glColor4f(1.0, 1.0, 1.0, 1.0);
    glEnable(GL_TEXTURE_2D);

    // ****************
    // The black squares marking location of grid elements
    // ****************
    glBindTexture(GL_TEXTURE_2D, media->gfx["gui_puzzle_cell_black"]->texture);

    // Recreate vertex lists if we should
    static vector< vector< vector<float> > > black_chunks;
    static vector< vector< vector<float> > > black_chunks_textures;

    // If resetting all chunks then clear every vector
    if(boost::python::extract<bool>(self_.attr("reset_drawing_all_blacks")))
    {
        black_chunks.clear();
        black_chunks_textures.clear();
        black_chunks.resize((int)ceil((float)current_puzzle_height / PUZZLE_RENDER_CHUNK_SIZE), vector< vector<float> >());
        black_chunks_textures.resize((int)ceil((float)current_puzzle_height / PUZZLE_RENDER_CHUNK_SIZE), vector< vector<float> >());

        BOOST_FOREACH(vector< vector<float> > &col, black_chunks)
            col.resize((int)ceil((float)current_puzzle_width / PUZZLE_RENDER_CHUNK_SIZE), vector<float>());
        BOOST_FOREACH(vector< vector<float> > &col, black_chunks_textures)
            col.resize((int)ceil((float)current_puzzle_width / PUZZLE_RENDER_CHUNK_SIZE), vector<float>());
    }
    else
    {

        // Check each individual chunk we need to potentially reset.
        boost::python::list black_chunks_to_redraw = boost::python::extract<boost::python::list>(self_.attr("black_chunks_to_redraw"));
    
        if(boost::python::len(black_chunks_to_redraw) > 0)
        {
            for(int i=0; i<boost::python::len(black_chunks_to_redraw); i++)
            {
                boost::python::tuple chunk_to_redraw = boost::python::extract<boost::python::tuple>(black_chunks_to_redraw[i]);
                black_chunks[boost::python::extract<int>(chunk_to_redraw[0])][boost::python::extract<int>(chunk_to_redraw[1])].clear();
                black_chunks_textures[boost::python::extract<int>(chunk_to_redraw[0])][boost::python::extract<int>(chunk_to_redraw[1])].clear();
            }
        }

    }

    // iterate through each chunk and add to the vertex list
    float draw_x;
    float draw_y;
    boost::python::list black_squares_to_ignore = boost::python::extract<boost::python::list>(self_.attr("black_squares_to_ignore"));
    bool do_ignore;

    // First we go through every chunk we could potentially draw
    for(int h=0; h < (int)black_chunks.size(); h++)
    {

        for(int w=0; w < (int)black_chunks[h].size(); w++)
        {

            // If the chunk has something in it then we can assume it's be filled with something. This is a pretty lazy way of doing it.
            if(black_chunks[h][w].size() > 0)
                continue;

            // We initialise the starting position along the x axis, according to which chunk this is 
            draw_x = (float)(PUZZLE_CELL_WIDTH * (PUZZLE_RENDER_CHUNK_SIZE * w));

            // Iterate through each column of this particular chunk
            for(int i = (w * PUZZLE_RENDER_CHUNK_SIZE); i < (w * PUZZLE_RENDER_CHUNK_SIZE) + PUZZLE_RENDER_CHUNK_SIZE; i++)
            {

                // Initialise where the y axis coordinate starts in this column
                draw_y = (float)(PUZZLE_CELL_HEIGHT * (PUZZLE_RENDER_CHUNK_SIZE * h));

                // Iterate through each row of this column in this chunk
                for(int j = (h * PUZZLE_RENDER_CHUNK_SIZE); j < (h * PUZZLE_RENDER_CHUNK_SIZE) + PUZZLE_RENDER_CHUNK_SIZE; j++)
                {

                    // If we're out of bounds then scoot out of here
                    if(j >= boost::python::len(current_puzzle_state) or i >= boost::python::len(current_puzzle_state[j]))
                        break;

                    // Sometimes we want to not draw certain squares, if those squares are being represented by dynamic
                    // processes, this chunk of code checks if the cell is to be ignored
                    do_ignore = False;
                    if(boost::python::len(black_squares_to_ignore) > 0)
                    {
                        for(int ign = 0; ign < boost::python::len(black_squares_to_ignore); ign++)
                        {
                            if(boost::python::extract<int>(black_squares_to_ignore[ign][0]) == j and boost::python::extract<int>(black_squares_to_ignore[ign][1]) == i)
                            {
                                do_ignore = True;
                                break;
                            }
                        }
                    }

                    // If this cell is not to be ignored and is currently set as True (as in, filled), then we add it to the vert lists
                    if(!do_ignore && boost::python::extract<bool>(current_puzzle_state[j][i]) == True)
                    {

                        // Add the verticies for this quad 
                        black_chunks[h][w].push_back(draw_x + (float)PUZZLE_CELL_WIDTH);
                        black_chunks[h][w].push_back(draw_y);

                        black_chunks[h][w].push_back(draw_x);
                        black_chunks[h][w].push_back(draw_y);

                        black_chunks[h][w].push_back(draw_x);
                        black_chunks[h][w].push_back(draw_y + (float)PUZZLE_CELL_HEIGHT);

                        black_chunks[h][w].push_back(draw_x + (float)PUZZLE_CELL_WIDTH);
                        black_chunks[h][w].push_back(draw_y + (float)PUZZLE_CELL_HEIGHT);

                        // Add the texture coordinates
                        black_chunks_textures[h][w].push_back(1.0); black_chunks_textures[h][w].push_back(0.0);
                        black_chunks_textures[h][w].push_back(0.0); black_chunks_textures[h][w].push_back(0.0);
                        black_chunks_textures[h][w].push_back(0.0); black_chunks_textures[h][w].push_back(1.0);
                        black_chunks_textures[h][w].push_back(1.0); black_chunks_textures[h][w].push_back(1.0);

                    }

                    // Move the y coordinate along one cell
                    draw_y += (float)PUZZLE_CELL_HEIGHT;

                }

                // Move the x coordinate along one cell
                draw_x += (float)PUZZLE_CELL_WIDTH;

            }

        }

    }

    // Now draw each chunk, assuming the chunks have things in them
    for(int h=0; h < (int)black_chunks.size(); h++)
    {

        for(int w=0; w < (int)black_chunks[h].size(); w++)
        {

            if(black_chunks[h][w].size() == 0)
                continue;

            glTexCoordPointer(2, GL_FLOAT, 0, &black_chunks_textures[h][w][0]);
            glVertexPointer(2, GL_FLOAT, 0, &black_chunks[h][w][0]);
            glDrawArrays(GL_QUADS, 0, (black_chunks[h][w].size() / 2));

        }

    }

    // ****************
    // The white squares marking location of blank squares
    // ****************
    glBindTexture(GL_TEXTURE_2D, media->gfx["gui_puzzle_cell_white"]->texture);

    // Recreate vertex lists if we should
    static vector< vector< vector<float> > > white_chunks;
    static vector< vector< vector<float> > > white_chunks_textures;

    // If resetting all chunks then clear every vector
    if(boost::python::extract<bool>(self_.attr("reset_drawing_all_whites")))
    {
        white_chunks.clear();
        white_chunks_textures.clear();
        white_chunks.resize((int)ceil((float)current_puzzle_height / PUZZLE_RENDER_CHUNK_SIZE), vector< vector<float> >());
        white_chunks_textures.resize((int)ceil((float)current_puzzle_height / PUZZLE_RENDER_CHUNK_SIZE), vector< vector<float> >());

        BOOST_FOREACH(vector< vector<float> > &col, white_chunks)
            col.resize((int)ceil((float)current_puzzle_width / PUZZLE_RENDER_CHUNK_SIZE), vector<float>());
        BOOST_FOREACH(vector< vector<float> > &col, white_chunks_textures)
            col.resize((int)ceil((float)current_puzzle_width / PUZZLE_RENDER_CHUNK_SIZE), vector<float>());
    }

    // Check each individual chunk we need to potentially reset.
    boost::python::list white_chunks_to_redraw = boost::python::extract<boost::python::list>(self_.attr("white_chunks_to_redraw"));

    if(boost::python::len(white_chunks_to_redraw) > 0)
    {
        for(int i=0; i<boost::python::len(white_chunks_to_redraw); i++)
        {
            boost::python::tuple chunk_to_redraw = boost::python::extract<boost::python::tuple>(
                white_chunks_to_redraw[i]
                );
            white_chunks[boost::python::extract<int>(chunk_to_redraw[0])]
                [boost::python::extract<int>(chunk_to_redraw[1])].clear();
            white_chunks_textures[boost::python::extract<int>(chunk_to_redraw[0])]
                [boost::python::extract<int>(chunk_to_redraw[1])].clear();
        }
    }

    // iterate through each chunk and add to the vertex list
    boost::python::list white_squares_to_ignore = boost::python::extract<boost::python::list>(self_.attr("white_squares_to_ignore"));

    // First we go through every chunk we could potentially draw
    for(int h=0; h < (int)white_chunks.size(); h++)
    {

        for(int w=0; w < (int)white_chunks[h].size(); w++)
        {

            // If the chunk has something in it then we can assume it's be filled with something. This is a pretty lazy way of doing it.
            if(white_chunks[h][w].size() > 0)
                continue;

            // We initialise the starting position along the x axis, according to which chunk this is 
            draw_x = (float)(PUZZLE_CELL_WIDTH * (PUZZLE_RENDER_CHUNK_SIZE * w));

            // Iterate through each column of this particular chunk
            for(int i = (w * PUZZLE_RENDER_CHUNK_SIZE); i < (w * PUZZLE_RENDER_CHUNK_SIZE) + PUZZLE_RENDER_CHUNK_SIZE; i++)
            {

                // Initialise where the y axis coordinate starts in this column
                draw_y = (float)(PUZZLE_CELL_HEIGHT * (PUZZLE_RENDER_CHUNK_SIZE * h));

                // Iterate through each row of this column in this chunk
                for(int j = (h * PUZZLE_RENDER_CHUNK_SIZE); j < (h * PUZZLE_RENDER_CHUNK_SIZE) + PUZZLE_RENDER_CHUNK_SIZE; j++)
                {

                    // If we're out of bounds then scoot out of here
                    if(j >= boost::python::len(current_puzzle_state) or i >= boost::python::len(current_puzzle_state[j]))
                        break;

                    // Sometimes we want to not draw certain squares, if those squares are being represented by dynamic
                    // processes, this chunk of code checks if the cell is to be ignored
                    do_ignore = False;
                    if(boost::python::len(white_squares_to_ignore) > 0)
                    {
                        for(int ign = 0; ign < boost::python::len(white_squares_to_ignore); ign++)
                        {
                            if(boost::python::extract<int>(white_squares_to_ignore[ign][0]) == j and boost::python::extract<int>(white_squares_to_ignore[ign][1]) == i)
                            {
                                do_ignore = True;
                                break;
                            }
                        }
                    }

                    // If this cell is not to be ignored and is currently set as False (as in, marked as not filled), then we add it to the vert lists
                    boost::python::object check = boost::python::extract<boost::python::object>(current_puzzle_state[j][i]);
                    if(!do_ignore && !check.is_none() && boost::python::extract<bool>(current_puzzle_state[j][i]) == False)
                    {

                        // Add the verticies for this quad 
                        white_chunks[h][w].push_back(draw_x + (float)PUZZLE_CELL_WIDTH);
                        white_chunks[h][w].push_back(draw_y);

                        white_chunks[h][w].push_back(draw_x);
                        white_chunks[h][w].push_back(draw_y);

                        white_chunks[h][w].push_back(draw_x);
                        white_chunks[h][w].push_back(draw_y + (float)PUZZLE_CELL_HEIGHT);

                        white_chunks[h][w].push_back(draw_x + (float)PUZZLE_CELL_WIDTH);
                        white_chunks[h][w].push_back(draw_y + (float)PUZZLE_CELL_HEIGHT);

                        // Add the texture coordinates
                        white_chunks_textures[h][w].push_back(1.0); white_chunks_textures[h][w].push_back(0.0);
                        white_chunks_textures[h][w].push_back(0.0); white_chunks_textures[h][w].push_back(0.0);
                        white_chunks_textures[h][w].push_back(0.0); white_chunks_textures[h][w].push_back(1.0);
                        white_chunks_textures[h][w].push_back(1.0); white_chunks_textures[h][w].push_back(1.0);

                    }

                    // Move the y coordinate along one cell
                    draw_y += (float)PUZZLE_CELL_HEIGHT;

                }

                // Move the x coordinate along one cell
                draw_x += (float)PUZZLE_CELL_WIDTH;

            }

        }

    }

    // Now draw each chunk, assuming the chunks have things in them
    for(int h=0; h < (int)white_chunks.size(); h++)
    {

        for(int w=0; w < (int)white_chunks[h].size(); w++)
        {

            if(white_chunks[h][w].size() == 0)
                continue;

            glTexCoordPointer(2, GL_FLOAT, 0, &white_chunks_textures[h][w][0]);
            glVertexPointer(2, GL_FLOAT, 0, &white_chunks[h][w][0]);
            glDrawArrays(GL_QUADS, 0, (white_chunks[h][w].size() / 2));

        }

    }

    // ****************
    // Reset matrix
    // ****************
    glPopMatrix();
    Process::current_bound_texture = -1;
    glTexCoordPointer(2, GL_FLOAT, 0, &Process::default_texture_coords[0]);

}


void Process::Draw_strategy_gui_designer_packs_pack_item()
{

    float width = boost::python::extract<float>(self_.attr("width"));
    float height = boost::python::extract<float>(self_.attr("height"));

    if(width == 0 || height == 0)
        return;

    tuple<float, float> draw_pos = get_screen_draw_position();
    float draw_x = draw_pos.get<0>();
    float draw_y = draw_pos.get<1>();

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    glPushMatrix();
    glDisable(GL_TEXTURE_2D);

    glColor4f(0.5, 0.5, 0.5, alpha);
    glBegin(GL_QUADS);
    glVertex2f(draw_x, draw_y);
    glVertex2f(width + draw_x, draw_y);
    glVertex2f(width + draw_x, height + draw_y);
    glVertex2f(draw_x, height + draw_y);
    glEnd();

    glColor4f(0.0, 0.0, 0.0, 1.0);
    glLineWidth(1.0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(draw_x, draw_y);
    glVertex2f(width + draw_x, draw_y);
    glVertex2f(width + draw_x, height + draw_y);
    glVertex2f(draw_x, height + draw_y);
    glEnd();

    glEnable(GL_TEXTURE_2D);
    glPopMatrix();

    // stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

}


/*
 *
 */
ProcessWrapper::ProcessWrapper(PyObject* _self) : Process()
{
    has_init = False;
    has_killed = False;
    is_dead = False;
    self = _self;
    self_ = boost::python::object(boost::python::handle<>(boost::python::borrowed(self)));
    Process::internal_list.append(self_);

    this->Process::self = self;
    this->Process::self_ = self_;
}


void ProcessWrapper::Kill()
{
    if(is_dead)
        return;
    boost::python::call_method<void>(self, "On_Exit");
    Process::internal_list.remove(self_);
    this->Process::Kill();
    boost::python::decref(self);
    boost::python::decref(self);
    self = NULL;
    is_dead = True;
    this->Process::is_dead = True;
}



void ProcessWrapper::Execute()
{
    boost::python::call_method<void>(self, "Execute");
}
void ProcessWrapper::Execute_default()
{
    this->Process::Execute();
}


void ProcessWrapper::On_Exit(){ }
void ProcessWrapper::On_Exit_default()
{
    this->Process::On_Exit();
}


tuple<float, float> ProcessWrapper::get_screen_draw_position()
{
    boost::python::object tup = boost::python::call_method<boost::python::object>(self, "get_screen_draw_position");
    return tuple<float, float>(boost::python::extract<float>(tup[0]), boost::python::extract<float>(tup[1]));
}
tuple<float, float> ProcessWrapper::get_screen_draw_position_default()
{
    return this->Process::get_screen_draw_position();
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
    Process::z = z;
    alignment = _alignment;
    shadow = 0;
    shadow_colour.resize(3, 1.0f);
    text_width = 0;
    text_height = 0;
    image_sequence = 1;
    scale = 1.0;
    rotation = 0;
    alpha = 1.0f;
    generate_mipmaps = False;

    set_text(_text);

}


Text::~Text()
{
    if(image != NULL)
        delete image;
    image = NULL;
}


void Text::Set_z(int new_z)
{
    z = new_z;
    Process::z = new_z;
    Process::z_order_dirty = True;
}


void Text::Set_colour(boost::python::object list)
{
    colour[0] = boost::python::extract<float>(list[0]);
    colour[1] = boost::python::extract<float>(list[1]);
    colour[2] = boost::python::extract<float>(list[2]);
}


void Text::Set_clip(boost::python::object list)
{
    clip[0] = boost::python::extract<float>(list[0]);
    clip[1] = boost::python::extract<float>(list[1]);
    clip[2] = boost::python::extract<float>(list[2]);
    clip[3] = boost::python::extract<float>(list[3]);
}


void Text::set_text(string new_text)
{

    text = new_text;
    generate_new_text_image();

}


void Text::Set_shadow_colour(boost::python::object list)
{
    shadow_colour[0] = boost::python::extract<float>(list[0]);
    shadow_colour[1] = boost::python::extract<float>(list[1]);
    shadow_colour[2] = boost::python::extract<float>(list[2]);
}


void Text::Set_generate_mipmaps(bool generate_mipmaps_)
{
    generate_mipmaps = generate_mipmaps_;
    generate_new_text_image();
}


void Text::generate_new_text_image()
{

    if(image != NULL)
        delete image;

    if(font == NULL || text == "")
    {
        image = NULL;
        return;
    }

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

    image = new Image(final_surface, generate_mipmaps);

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


void Text::Draw()
{

    if(is_dead == True || image == NULL)
        return;

    glPushMatrix();

    // Get drawing coords
    tuple<float, float> draw_pos = get_screen_draw_position();

    // Clip the process if necessary
    if(clip[2] > 0 and clip[3] > 0)
    {
        glEnable(GL_SCISSOR_TEST);
        glScissor(
            clip[0],
            Main_App::screen_height - clip[1] - clip[3],
            clip[2],
            clip[3]
            );
    }

    // glrotate works by you translating to the point around which you wish to rotate
    // and applying the rotation you can translate back to apply the real translation
    // position
    if(rotation < 0 || rotation > 0)
    {
        float rot_x = (draw_pos.get<0>() * scale) + ((image->width/2) * scale);
        float rot_y = (draw_pos.get<1>() * scale) + ((image->height/2) * scale);
        glTranslatef(rot_x, rot_y, 0.0f);
        glRotatef((float)rotation, 0.0f, 0.0f, 1.0f);
        glTranslatef(-rot_x, -rot_y, 0.0f);
    }

    // move to position
    glTranslatef(draw_pos.get<0>(), draw_pos.get<1>(), 0.0f);

    // scaling
    if(scale < 1.0f || scale > 1.0f)
    {
        glTranslatef(scale_pos[0], scale_pos[1], 0.0f);
        glScalef(scale, scale, 1.0f);
        glTranslatef(-scale_pos[0], -scale_pos[1], 0.0f);
    }
                               
    // Binding texture
    if(Process::current_bound_texture != image->texture)
    {
        glBindTexture(GL_TEXTURE_2D, image->texture);
        glVertexPointer(3, GL_FLOAT, 0, image->vertex_list);
        Process::current_bound_texture = image->texture;
    }

    // Shadow stuff
    if(shadow > 0)
    {
        glTranslatef(shadow, shadow, 0.0f);
        glColor4f(shadow_colour[0], shadow_colour[1], shadow_colour[2], alpha);
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
        glTranslatef(-shadow, -shadow, 0.0f);
    }

    // Changing colour and transparency
    glColor4f(colour[0], colour[1], colour[2], alpha);

    // draw the triangle strip
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    // Stop clipping
    if(clip[2] > 0 and clip[3] > 0)
        glDisable(GL_SCISSOR_TEST);

    glPopMatrix();

}


/*
 *
 */
void TextWrapper::Execute(){}
void TextWrapper::Execute_default()
{
    this->Text::Execute();
}



void TextWrapper::Kill()
{
    if(is_dead)
        return;
    Process::internal_list.remove(self_);
    this->Process::Kill();
    boost::python::decref(self);
    boost::python::decref(self);
    self = NULL;
    is_dead = True;
    this->Process::is_dead = True;
}


TextWrapper::TextWrapper(PyObject* _self, Font* _font, float _x, float _y, int _alignment, string _text) : Text(_font, _x, _y, _alignment, _text)
{
    self = _self;
    self_ = boost::python::object(boost::python::handle<>(boost::python::borrowed(self)));
    Process::internal_list.append(self_);
}



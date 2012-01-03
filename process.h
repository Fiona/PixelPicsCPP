/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Processesss
 ****************************/


#ifndef _PROCESS_H_
#define _PROCESS_H_

using namespace boost;

#include <vector>
#include <SDL/SDL.h>


#define TEXT_ALIGN_TOP_LEFT 0
#define TEXT_ALIGN_TOP 1
#define TEXT_ALIGN_TOP_RIGHT 2
#define TEXT_ALIGN_CENTER_LEFT 3
#define TEXT_ALIGN_CENTER 4
#define TEXT_ALIGN_CENTER_RIGHT 5
#define TEXT_ALIGN_BOTTOM_LEFT 6
#define TEXT_ALIGN_BOTTOM 7
#define TEXT_ALIGN_BOTTOM_RIGHT 8 

#define Z_TEXT -512


/*
 */
class Process
{

public:
    static std::vector<Process*> Process_List;
    static bool z_order_dirty;
    static GLuint current_bound_texture;

    static std::vector<Process*> Processes_to_kill;

    float   x;
    float   y;
    int     z;
    Image*  image;
 
    Process();
    virtual ~Process();
    virtual void Execute();
    virtual void Draw();

    void Kill();

    void move_forward(float distance_to_travel, int rotation_to_move_in);
    float deg_to_rad(float deg);
    float rad_to_deg(float rad);

    virtual tuple<float, float> get_screen_draw_position();

};


/*
 */
class Text: public Process
{

public:
    Text(Font* _font, float _x, float _y, int _alignment, string _text);

    Font* font;
    int alignment;    
    string text;

    int text_width;
    int text_height;

    void set_text(string _text);

    tuple<float, float> get_screen_draw_position();

private:
    void generate_new_text_image();

};


#endif 

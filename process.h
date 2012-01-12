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

struct ProcessWrapper;

/*
 */
class Process
{

public:
    Process();
    virtual ~Process();

    static boost::python::list internal_list;

    static std::vector<Process*> Process_List;
    static bool z_order_dirty;
    static GLuint current_bound_texture;

    static void Initialise_draw_strategies();

    static std::vector<Process*> Processes_to_kill;

    // Draw strategies
    void Draw_strategy_primitive_square();

    float   x;
    float   y;
    int     z;
    Image*  image;
    float   scale;
    int rotation;
    std::vector<float> colour;
    float alpha;
    int image_sequence;

    string draw_strategy;
    PyObject* self;

    virtual void Init();
    virtual void Execute();
    virtual void On_Exit();
    virtual void Draw();

    void Kill();

    void Set_colour(boost::python::object list);

    void move_forward(float distance_to_travel, int rotation_to_move_in);
    float deg_to_rad(float deg);
    float rad_to_deg(float rad);

    virtual tuple<float, float> get_screen_draw_position();

};


struct ProcessWrapper : Process
{

    ProcessWrapper(PyObject *p);

    bool has_init;
    bool has_killed;
    PyObject *self;
    boost::python::object self_hold;

    ProcessWrapper();
    void Init();
    void Init_default();
    void Execute();
    void Execute_default();
    void On_Exit();
    void On_Exit_default();
    void Kill();

};


/*
 */
class Text: public Process
{

public:
    Text();
    Text(Font* _font, float _x, float _y, int _alignment, string _text);
    ~Text();

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


struct TextWrapper : Text
{

    TextWrapper(PyObject *p);
    TextWrapper(PyObject *p, Font* _font, float _x, float _y, int _alignment, string _text);

    PyObject *self;

    void Execute();
    void Execute_default();

};


#endif 

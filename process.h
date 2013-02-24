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
    static std::vector<Process*> Priority_List;
    static bool priority_order_dirty;
    static GLuint current_bound_texture;

    static vector<float> default_texture_coords;
    static std::vector<Process*> Processes_to_kill;

    float   x;
    float   y;
    int     z;
    int priority;
    Image*  image;
    float   scale;
    int rotation;
    std::vector<float> colour;
    std::vector<float> clip;
    float alpha;
    int image_sequence;
    std::vector<float> scale_pos;
    
    bool is_dead;

    string draw_strategy;
    PyObject* self;
    boost::python::object self_;

    virtual void Execute();
    virtual void On_Exit();
    virtual void Draw();

    void Kill();

    void Set_z(int new_z);
    void Set_priority(int priority_);
    void Set_colour(boost::python::object list);
    void Set_clip(boost::python::object list);
    void Set_scale_pos(boost::python::object list);

    void move_forward(float distance_to_travel, int rotation_to_move_in);
    float deg_to_rad(float deg);
    float rad_to_deg(float rad);

    virtual tuple<float, float> get_screen_draw_position();

    // Draw strategies
    void Draw_strategy_primitive_square();
    void Draw_strategy_primitive_line();
    void Draw_strategy_gui_button();
    void Draw_strategy_gui_window_frame();
    void Draw_strategy_gui_text_input();
    void Draw_strategy_gui_dropdown_currently_selected();
    void Draw_strategy_gui_dropdown_options();
    void Draw_strategy_puzzle();
    void Draw_strategy_puzzle_pixel_message();
    void Draw_strategy_gui_scroll_window();
    void Draw_strategy_gui_designer_packs_pack_item();
    void Draw_strategy_gui_spinner();
    void Draw_strategy_gui_slider();
    void Draw_strategy_gui_designer_designer_menu_bar();
    void Draw_strategy_gui_designer_monochrome_puzzle_image();
    void Draw_strategy_designer_puzzle_background_item();
    void Draw_strategy_designer_colour_current_colour();
    void Draw_strategy_designer_colour_value_slider();
    void Draw_strategy_balloons_background();
    void Draw_strategy_tutorial_background();
    void Draw_strategy_designer_background();
    void Draw_strategy_puzzle_select();
    void Draw_strategy_puzzle_select_puzzle_item();
    void Draw_strategy_main_menu_title();
    void create_image_from_puzzle();
    void destroy_puzzle_image();
    void create_image_as_pallete(int pallete_width, int pallete_height);

};


struct ProcessWrapper : Process
{

    ProcessWrapper(PyObject *p);
    ProcessWrapper();

    bool has_init;
    bool has_killed;
    bool is_dead;
    PyObject *self;
    boost::python::object self_;

    void Execute();
    void Execute_default();
    void On_Exit();
    void On_Exit_default();
    void Kill();
    tuple<float, float> get_screen_draw_position();
    tuple<float, float> get_screen_draw_position_default();

};


/*
 */
class Text: public Process
{

public:
    Text();
    Text(Font* _font, float _x, float _y, int _alignment, string _text);
    ~Text();

    float   x;
    float   y;
    int     z;
    int     priority;
    float   scale;
    int rotation;
    float alpha;

    Font* font;
    int alignment;    
    string text;
    int text_width;
    int text_height;
    int shadow;
    std::vector<float> shadow_colour;
    bool generate_mipmaps;

    void Set_z(int new_z);
    void set_text(string _text);
    void Set_colour(boost::python::object list);
    void Set_clip(boost::python::object list);
    void Set_shadow_colour(boost::python::object list);
    void Set_generate_mipmaps(bool generate_mipmaps_);
    tuple<float, float> get_screen_draw_position();

    void Draw();
    void Kill();

private:
    void generate_new_text_image();

};


struct TextWrapper : Text
{

    TextWrapper(PyObject *p);
    TextWrapper(PyObject *p, Font* _font, float _x, float _y, int _alignment, string _text);

    PyObject *self;
    boost::python::object self_;

    void Execute();
    void Execute_default();
    void Kill();

};



#endif 

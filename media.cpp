/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Media object source file
 ****************************/


#include <string>
using namespace std;

#include "main.h"


Media::Media()
{

    // Load all the fonts!
    fonts.insert(pair<string,Font*>("basic", new Font("fnt/arulent.ttf", 13)));
    fonts.insert(pair<string,Font*>("small", new Font("fnt/bitmap1.ttf", 10)));
    fonts.insert(pair<string,Font*>("puzzle_hint_numbers", new Font("fnt/borisblackbloxx.ttf", 40)));
    fonts.insert(pair<string,Font*>("puzzle_message", new Font("fnt/aurulent.ttf", 25)));
    fonts.insert(pair<string,Font*>("puzzle_timer", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("menu_titles", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("menu_subtitles", new Font("fnt/borisblackbloxx.ttf", 25)));
    fonts.insert(pair<string,Font*>("designer_pack_name", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("designer_pack_author", new Font("fnt/borisblackbloxx.ttf", 15)));
    fonts.insert(pair<string,Font*>("verifier_status", new Font("fnt/borisblackbloxx.ttf", 16)));

    // Visuals
    //gfx.insert(pair<string, Image*>("blank", new Image("gfx/gui/stompyblondie_logo.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo", new Image("gfx/gui/stompyblondie_logo.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_text", new Image("gfx/gui/stompyblondie_logo_text.png")));

    gfx.insert(pair<string, Image*>("gui_cursor_1", new Image("gfx/gui/cursor_tool_1.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_2", new Image("gfx/gui/cursor_tool_2.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_3", new Image("gfx/gui/cursor_tool_3.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_4", new Image("gfx/gui/cursor_tool_4.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_5", new Image("gfx/gui/cursor_tool_5.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_6", new Image("gfx/gui/cursor_tool_6.png")));

    gfx.insert(pair<string, Image*>("gui_button_generic_background", new Image("gfx/gui/button_generic_background.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_down", new Image("gfx/gui/button_spinner_down.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_up", new Image("gfx/gui/button_spinner_up.png", 3)));
    gfx.insert(pair<string, Image*>("gui_dropdown_arrrow", new Image("gfx/gui/dropdown_arrrow.png", 3)));

    gfx.insert(pair<string, Image*>("gui_main_menu_title_pixel", new Image("gfx/gui/main_menu_title_pixel.png")));
    gfx.insert(pair<string, Image*>("gui_main_menu_background", new Image("gfx/gui/main_menu_background.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_mini", new Image("gfx/gui/stompyblondie_logo_mini.png", 2)));

    gfx.insert(pair<string, Image*>("gui_puzzle_grid_background", new Image("gfx/gui/puzzle_grid_background.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_white", new Image("gfx/gui/puzzle_cell_white.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_black", new Image("gfx/gui/puzzle_cell_black.png")));

    gfx.insert(pair<string, Image*>("gui_heart", new Image("gfx/gui/heart.png", 2)));

    gfx.insert(pair<string, Image*>("gui_verify_status", new Image("gfx/gui/verify_status.png", 3)));

    gfx.insert(pair<string, Image*>("gui_button_scroll_window_arrow", new Image("gfx/gui/button_scroll_window_arrow.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_edit", new Image("gfx/gui/button_designer_edit.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_detele", new Image("gfx/gui/button_designer_delete.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_down", new Image("gfx/gui/button_designer_move_down.png", 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_up", new Image("gfx/gui/button_designer_move_up.png", 3)));

}


Media::~Media()
{

    for(map<string, Image* >::iterator it = gfx.begin(); it != gfx.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        delete it->second;
    }

    for(map<string, Font* >::iterator it = fonts.begin(); it != fonts.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        delete it->second;
    }

}

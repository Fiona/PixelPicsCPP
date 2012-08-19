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
    fonts.insert(pair<string,Font*>("puzzle_message", new Font("fnt/arulent.ttf", 25)));
    fonts.insert(pair<string,Font*>("puzzle_timer", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("menu_titles", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("menu_subtitles", new Font("fnt/borisblackbloxx.ttf", 25)));
    fonts.insert(pair<string,Font*>("designer_pack_name", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("designer_pack_author", new Font("fnt/borisblackbloxx.ttf", 15)));
    fonts.insert(pair<string,Font*>("verifier_status", new Font("fnt/borisblackbloxx.ttf", 16)));
    fonts.insert(pair<string,Font*>("category_button_name", new Font("fnt/borisblackbloxx.ttf", 36)));
    fonts.insert(pair<string,Font*>("category_button_completed_count", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("category_button_total_count", new Font("fnt/borisblackbloxx.ttf", 12)));
    fonts.insert(pair<string,Font*>("speech_bubble", new Font("fnt/cookies.ttf", 20)));
    fonts.insert(pair<string,Font*>("puzzle_select_number", new Font("fnt/cookies.ttf", 30)));
    fonts.insert(pair<string,Font*>("puzzle_select_size", new Font("fnt/bitmap1.ttf", 12)));
    fonts.insert(pair<string,Font*>("options_title", new Font("fnt/arulent.ttf", 15)));

    // Visuals
    //gfx.insert(pair<string, Image*>("blank", new Image("gfx/gui/stompyblondie_logo.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo", new Image("gfx/gui/stompyblondie_logo.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_text", new Image("gfx/gui/stompyblondie_logo_text.png")));

    gfx.insert(pair<string, Image*>("gui_cursor_1", new Image("gfx/gui/cursor_tool_1.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_2", new Image("gfx/gui/cursor_tool_2.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_3", new Image("gfx/gui/cursor_tool_3.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_4", new Image("gfx/gui/cursor_tool_4.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_5", new Image("gfx/gui/cursor_tool_5.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_6", new Image("gfx/gui/cursor_tool_6.png")));

    gfx.insert(pair<string, Image*>("gui_button_generic_background", new Image("gfx/gui/button_generic_background.png", True, 4)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_down", new Image("gfx/gui/button_spinner_down.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_up", new Image("gfx/gui/button_spinner_up.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_dropdown_arrow", new Image("gfx/gui/dropdown_arrow.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_radio_button", new Image("gfx/gui/radio_button.png", True, 4)));
    gfx.insert(pair<string, Image*>("gui_slider_handle", new Image("gfx/gui/slider_handle.png", True, 2)));

    gfx.insert(pair<string, Image*>("gui_main_menu_title_pixel", new Image("gfx/gui/main_menu_title_pixel.png")));
    gfx.insert(pair<string, Image*>("gui_main_menu_background", new Image("gfx/gui/main_menu_background.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_mini", new Image("gfx/gui/stompyblondie_logo_mini.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_puzzle_grid_background", new Image("gfx/gui/puzzle_grid_background.png", True)));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_white", new Image("gfx/gui/puzzle_cell_white.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_black", new Image("gfx/gui/puzzle_cell_black.png")));

    gfx.insert(pair<string, Image*>("gui_heart", new Image("gfx/gui/heart.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_verify_status", new Image("gfx/gui/verify_status.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_button_scroll_window_arrow", new Image("gfx/gui/button_scroll_window_arrow.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_edit", new Image("gfx/gui/button_designer_edit.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_delete", new Image("gfx/gui/button_designer_delete.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_down", new Image("gfx/gui/button_designer_move_down.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_up", new Image("gfx/gui/button_designer_move_up.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_palette_cursor", new Image("gfx/gui/palette_cursor.png")));
    gfx.insert(pair<string, Image*>("gui_value_slider", new Image("gfx/gui/value_slider.png")));

    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_main", new Image("gfx/gui/button_puzzle_type_select_main.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_downloaded", new Image("gfx/gui/button_puzzle_type_select_downloaded.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_go_back", new Image("gfx/gui/button_go_back.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category", new Image("gfx/gui/button_select_category.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category_unlock_mask", new Image("gfx/gui/button_select_category_unlock_mask.png")));
    gfx.insert(pair<string, Image*>("gui_category_complete_tick", new Image("gfx/gui/category_complete_tick.png")));
    gfx.insert(pair<string, Image*>("gui_category_locked", new Image("gfx/gui/category_locked.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_polka", new Image("gfx/gui/polka.png", True)));
    gfx.insert(pair<string, Image*>("gui_stars", new Image("gfx/gui/stars.png", True)));

    gfx.insert(pair<string, Image*>("gui_puzzle_image_unsolved", new Image("gfx/gui/puzzle_image_unsolved.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_solved_icon", new Image("gfx/gui/puzzle_select_solved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_saved_icon", new Image("gfx/gui/puzzle_select_saved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_star_icon", new Image("gfx/gui/puzzle_select_star_icon.png")));

    gfx.insert(pair<string, Image*>("gui_chips_happy", new Image("gfx/gui/chips_happy.png")));
    gfx.insert(pair<string, Image*>("gui_speech_bubble", new Image("gfx/gui/speech_bubble.png")));
 
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

/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Media object source file
 ****************************/


#include <string>
using namespace std;

#include "main.h"


void channel_finished_playing(int channel)
{
    
    for(map<string, SFX* >::iterator it = Main_App::media->sfx.begin(); it != Main_App::media->sfx.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        if(it->second->channel == channel)
            it->second->channel = -1;
    }

}


Media::Media()
{
    game = NULL;
}


Media::Media(Main_App* _game)
{

    game = _game;
    Mix_ChannelFinished(channel_finished_playing);

    // Load all the fonts!
    fonts.insert(pair<string,Font*>("basic", new Font("fnt/arulent.ttf", 13)));
    fonts.insert(pair<string,Font*>("small", new Font("fnt/bitmap1.ttf", 10)));
    fonts.insert(pair<string,Font*>("window_title", new Font("fnt/borisblackbloxx.ttf", 25)));
    fonts.insert(pair<string,Font*>("window_subtitle", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("window_text", new Font("fnt/designosaur.ttf", 18)));
    fonts.insert(pair<string,Font*>("generic_buttons", new Font("fnt/borisblackbloxx.ttf", 14)));
    fonts.insert(pair<string,Font*>("dropdown_text", new Font("fnt/designosaur.ttf", 17)));
    fonts.insert(pair<string,Font*>("dropdown_text_options", new Font("fnt/designosaur.ttf", 15)));
    fonts.insert(pair<string,Font*>("text_input", new Font("fnt/bitstreamverasansmono.ttf", 15)));
    fonts.insert(pair<string,Font*>("puzzle_hint_numbers", new Font("fnt/borisblackbloxx.ttf", 40)));
    fonts.insert(pair<string,Font*>("puzzle_message", new Font("fnt/arulent.ttf", 25)));
    fonts.insert(pair<string,Font*>("puzzle_timer", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("menu_titles", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("menu_subtitles", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("designer_pack_name", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("designer_pack_author", new Font("fnt/borisblackbloxx.ttf", 15)));
    fonts.insert(pair<string,Font*>("verifier_status", new Font("fnt/borisblackbloxx.ttf", 16)));
    fonts.insert(pair<string,Font*>("category_button_name", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("category_button_completed_count", new Font("fnt/borisblackbloxx.ttf", 28)));
    fonts.insert(pair<string,Font*>("category_button_solved_text", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("speech_bubble", new Font("fnt/cookies.ttf", 20)));
    fonts.insert(pair<string,Font*>("puzzle_select_number", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("puzzle_select_size", new Font("fnt/bitmap1.ttf", 12)));
    fonts.insert(pair<string,Font*>("options_mouse_button", new Font("fnt/designosaur.ttf", 15)));
    fonts.insert(pair<string,Font*>("tutorial_instructions", new Font("fnt/basiccomical.ttf", 25)));
    fonts.insert(pair<string,Font*>("tutorial_click_to_continue", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("title_speech_bubble", new Font("fnt/basiccomical.ttf", 20)));
    fonts.insert(pair<string,Font*>("category_select_speech_bubble", new Font("fnt/basiccomical.ttf", 30)));

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
    gfx.insert(pair<string, Image*>("gui_dropdown_arrow", new Image("gfx/gui/dropdown_arrow.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_radio_button", new Image("gfx/gui/radio_button.png", True, 4)));
    gfx.insert(pair<string, Image*>("gui_slider_handle", new Image("gfx/gui/slider_handle.png", True, 4)));

    gfx.insert(pair<string, Image*>("gui_main_menu_title_pixel", new Image("gfx/gui/main_menu_title_pixel.png")));
    gfx.insert(pair<string, Image*>("gui_main_menu_background", new Image("gfx/gui/main_menu_background.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_mini", new Image("gfx/gui/stompyblondie_logo_mini.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_reward_star", new Image("gfx/gui/reward_star.png")));

    gfx.insert(pair<string, Image*>("gui_title_bg", new Image("gfx/gui/title_bg.png")));
    gfx.insert(pair<string, Image*>("gui_title_p", new Image("gfx/gui/title_p.png")));
    gfx.insert(pair<string, Image*>("gui_title_i", new Image("gfx/gui/title_i.png")));
    gfx.insert(pair<string, Image*>("gui_title_x", new Image("gfx/gui/title_x.png", False, 6)));
    gfx.insert(pair<string, Image*>("gui_title_e", new Image("gfx/gui/title_e.png")));
    gfx.insert(pair<string, Image*>("gui_title_l", new Image("gfx/gui/title_l.png")));
    gfx.insert(pair<string, Image*>("gui_title_c", new Image("gfx/gui/title_c.png")));
    gfx.insert(pair<string, Image*>("gui_title_s", new Image("gfx/gui/title_s.png")));

    gfx.insert(pair<string, Image*>("gui_title_speech_bubble", new Image("gfx/gui/title_speech_bubble.png")));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_play", new Image("gfx/gui/button_main_menu_play.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_extras", new Image("gfx/gui/button_main_menu_extras.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_options", new Image("gfx/gui/button_main_menu_options.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_designer", new Image("gfx/gui/button_main_menu_designer.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_quit", new Image("gfx/gui/button_main_menu_quit.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_tutorial", new Image("gfx/gui/button_main_menu_tutorial.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_scroll_button_down", new Image("gfx/gui/scroll_button_down.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_scroll_button_up", new Image("gfx/gui/scroll_button_up.png", False, 4)));

    gfx.insert(pair<string, Image*>("gui_puzzle_grid_background", new Image("gfx/gui/puzzle_grid_background.png", True)));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_white", new Image("gfx/gui/puzzle_cell_white.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_black", new Image("gfx/gui/puzzle_cell_black.png")));

    gfx.insert(pair<string, Image*>("gui_heart", new Image("gfx/gui/heart.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_verify_status", new Image("gfx/gui/verify_status.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_button_designer_edit", new Image("gfx/gui/button_designer_edit.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_delete", new Image("gfx/gui/button_designer_delete.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_down", new Image("gfx/gui/button_designer_move_down.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_up", new Image("gfx/gui/button_designer_move_up.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_palette_cursor", new Image("gfx/gui/palette_cursor.png")));
    gfx.insert(pair<string, Image*>("gui_value_slider", new Image("gfx/gui/value_slider.png")));

    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_main", new Image("gfx/gui/button_puzzle_type_select_main.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_downloaded", new Image("gfx/gui/button_puzzle_type_select_downloaded.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_go_back", new Image("gfx/gui/button_go_back.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category", new Image("gfx/gui/button_select_category.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category_shadow", new Image("gfx/gui/button_select_category_shadow.png")));
    gfx.insert(pair<string, Image*>("gui_button_select_category_unlock_mask", new Image("gfx/gui/button_select_category_unlock_mask.png")));
    gfx.insert(pair<string, Image*>("gui_category_complete_tick", new Image("gfx/gui/category_complete_tick.png")));
    gfx.insert(pair<string, Image*>("gui_category_complete_star", new Image("gfx/gui/category_complete_star.png")));
    gfx.insert(pair<string, Image*>("gui_category_locked", new Image("gfx/gui/category_locked.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_background_present", new Image("gfx/gui/background_present.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_balloons", new Image("gfx/gui/background_balloons.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_grid", new Image("gfx/gui/background_grid.png", True)));
    gfx.insert(pair<string, Image*>("gui_stars", new Image("gfx/gui/stars.png", True)));
    gfx.insert(pair<string, Image*>("gui_mouse", new Image("gfx/gui/mouse.png")));

    gfx.insert(pair<string, Image*>("gui_puzzle_image_unsolved", new Image("gfx/gui/puzzle_image_unsolved.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_puzzle_box", new Image("gfx/gui/puzzle_select_puzzle_box.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_solved_icon", new Image("gfx/gui/puzzle_select_solved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_saved_icon", new Image("gfx/gui/puzzle_select_saved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_star_icon", new Image("gfx/gui/puzzle_select_star_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_rating_star", new Image("gfx/gui/puzzle_select_rating_star.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_sharing_rating_stars", new Image("gfx/gui/sharing_rating_stars.png", False, 6)));

    gfx.insert(pair<string, Image*>("gui_chips_normal", new Image("gfx/gui/chips_normal.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_chips_happy", new Image("gfx/gui/chips_happy.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_chips_sad", new Image("gfx/gui/chips_sad.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_speech_bubble", new Image("gfx/gui/speech_bubble.png")));

    gfx.insert(pair<string, Image*>("gui_button_sharing_upload", new Image("gfx/gui/button_sharing_upload.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_download", new Image("gfx/gui/button_sharing_download.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_play", new Image("gfx/gui/button_sharing_play.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_delete", new Image("gfx/gui/button_sharing_delete.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_next", new Image("gfx/gui/button_sharing_next.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_prev", new Image("gfx/gui/button_sharing_prev.png", False, 3)));

    // Sound effects!
    sfx.insert(pair<string,SFX*>("empty_square", new SFX("sfx/empty_square.wav", game, False)));
    sfx.insert(pair<string,SFX*>("fill_square", new SFX("sfx/fill_square.wav", game, False)));
    sfx.insert(pair<string,SFX*>("incorrect_square", new SFX("sfx/incorrect_square.wav", game)));
    sfx.insert(pair<string,SFX*>("failure", new SFX("sfx/failure.wav", game)));
    sfx.insert(pair<string,SFX*>("success", new SFX("sfx/success.wav", game)));
    sfx.insert(pair<string,SFX*>("unlock", new SFX("sfx/unlock.wav", game)));
    sfx.insert(pair<string,SFX*>("button_click", new SFX("sfx/button_click.wav", game)));
    sfx.insert(pair<string,SFX*>("button_hover", new SFX("sfx/button_hover.wav", game)));
    sfx.insert(pair<string,SFX*>("meow1", new SFX("sfx/meow1.wav", game, False)));
    sfx.insert(pair<string,SFX*>("type", new SFX("sfx/type.wav", game)));
    sfx.insert(pair<string,SFX*>("paint", new SFX("sfx/paint.wav", game, False)));
    sfx.insert(pair<string,SFX*>("fill", new SFX("sfx/fill.wav", game)));
    sfx.insert(pair<string,SFX*>("pipette", new SFX("sfx/pipette.wav", game)));

    // Music
    music.insert(pair<string,Music*>("title", new Music("music/title.ogg", game)));
    music.insert(pair<string,Music*>("select_puzzle", new Music("music/select_puzzle.ogg", game)));
    music.insert(pair<string,Music*>("puzzle", new Music("music/puzzle.ogg", game)));
    music.insert(pair<string,Music*>("editor", new Music("music/editor.ogg", game)));

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

    for(map<string, SFX* >::iterator it = sfx.begin(); it != sfx.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        delete it->second;
    }

    for(map<string, Music* >::iterator it = music.begin(); it != music.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        delete it->second;
    }

}

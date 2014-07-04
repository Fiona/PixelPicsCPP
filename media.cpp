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
    fonts.insert(pair<string,Font*>("puzzle_message", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("puzzle_special_icons", new Font("fnt/borisblackbloxx.ttf", 40)));
    fonts.insert(pair<string,Font*>("puzzle_timer", new Font("fnt/timer_mono.ttf", 25)));
    fonts.insert(pair<string,Font*>("puzzle_click_to_continue", new Font("fnt/basiccomical.ttf", 40)));
    fonts.insert(pair<string,Font*>("menu_titles", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("menu_subtitles", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("menu_titles_small", new Font("fnt/borisblackbloxx.ttf", 24)));
    fonts.insert(pair<string,Font*>("menu_subtitles_small", new Font("fnt/borisblackbloxx.ttf", 18)));
    fonts.insert(pair<string,Font*>("designer_pack_name", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("designer_pack_author", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("verifier_status", new Font("fnt/borisblackbloxx.ttf", 16)));
    fonts.insert(pair<string,Font*>("category_button_name", new Font("fnt/borisblackbloxx.ttf", 35)));
    fonts.insert(pair<string,Font*>("category_button_completed_count", new Font("fnt/borisblackbloxx.ttf", 28)));
    fonts.insert(pair<string,Font*>("category_button_solved_text", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("category_button_total_count", new Font("fnt/borisblackbloxx.ttf", 22)));
    fonts.insert(pair<string,Font*>("speech_bubble", new Font("fnt/cookies.ttf", 20)));
    fonts.insert(pair<string,Font*>("puzzle_select_number", new Font("fnt/borisblackbloxx.ttf", 30)));
    fonts.insert(pair<string,Font*>("puzzle_select_size", new Font("fnt/bitmap1.ttf", 12)));
    fonts.insert(pair<string,Font*>("options_mouse_button", new Font("fnt/designosaur.ttf", 15)));
    fonts.insert(pair<string,Font*>("tutorial_instructions", new Font("fnt/basiccomical.ttf", 25)));
    fonts.insert(pair<string,Font*>("tutorial_click_to_continue", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("title_speech_bubble", new Font("fnt/basiccomical.ttf", 20)));
    fonts.insert(pair<string,Font*>("category_select_speech_bubble", new Font("fnt/basiccomical.ttf", 30)));
    fonts.insert(pair<string,Font*>("puzzle_select_speech_bubble", new Font("fnt/basiccomical.ttf", 35)));
    fonts.insert(pair<string,Font*>("puzzle_select_hover_text", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("puzzle_select_rate_pack_text", new Font("fnt/borisblackbloxx.ttf", 20)));
    fonts.insert(pair<string,Font*>("sharing_page_number", new Font("fnt/borisblackbloxx.ttf", 23)));
    fonts.insert(pair<string,Font*>("sharing_your_pack_message", new Font("fnt/borisblackbloxx.ttf", 25)));

    // Visuals
    //gfx.insert(pair<string, Image*>("blank", new Image("gfx/stompyblondie_logo.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo", new Image("gfx/stompyblondie_logo.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_text", new Image("gfx/stompyblondie_logo_text.png")));

    gfx.insert(pair<string, Image*>("gui_cursor_1", new Image("gfx/cursor_tool_1.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_2", new Image("gfx/cursor_tool_2.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_3", new Image("gfx/cursor_tool_3.png")));
    gfx.insert(pair<string, Image*>("gui_cursor_4", new Image("gfx/cursor_tool_4.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_5", new Image("gfx/cursor_tool_5.png")));
    //gfx.insert(pair<string, Image*>("gui_cursor_6", new Image("gfx/cursor_tool_6.png")));

    gfx.insert(pair<string, Image*>("gui_button_generic_background", new Image("gfx/button_generic_background.png", True, 4)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_down", new Image("gfx/button_spinner_down.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_spinner_up", new Image("gfx/button_spinner_up.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_dropdown_arrow", new Image("gfx/dropdown_arrow.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_radio_button", new Image("gfx/radio_button.png", True, 4)));
    gfx.insert(pair<string, Image*>("gui_slider_handle", new Image("gfx/slider_handle.png", True, 4)));

    gfx.insert(pair<string, Image*>("gui_main_menu_title_pixel", new Image("gfx/main_menu_title_pixel.png")));
    gfx.insert(pair<string, Image*>("gui_main_menu_background", new Image("gfx/main_menu_background.png")));
    gfx.insert(pair<string, Image*>("gui_stompyblondie_logo_mini", new Image("gfx/stompyblondie_logo_mini.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_reward_star", new Image("gfx/reward_star.png")));

    gfx.insert(pair<string, Image*>("gui_title_bg", new Image("gfx/title_bg.png")));
    gfx.insert(pair<string, Image*>("gui_title_p", new Image("gfx/title_p.png")));
    gfx.insert(pair<string, Image*>("gui_title_i", new Image("gfx/title_i.png")));
    gfx.insert(pair<string, Image*>("gui_title_x", new Image("gfx/title_x.png", False, 6)));
    gfx.insert(pair<string, Image*>("gui_title_e", new Image("gfx/title_e.png")));
    gfx.insert(pair<string, Image*>("gui_title_e_normal", new Image("gfx/title_e_normal.png")));
    gfx.insert(pair<string, Image*>("gui_title_l", new Image("gfx/title_l.png")));
    gfx.insert(pair<string, Image*>("gui_title_c", new Image("gfx/title_c.png")));
    gfx.insert(pair<string, Image*>("gui_title_s", new Image("gfx/title_s.png")));
    gfx.insert(pair<string, Image*>("gui_title_F", new Image("gfx/title_uppercase_f.png")));
    gfx.insert(pair<string, Image*>("gui_title_a", new Image("gfx/title_a.png")));
    gfx.insert(pair<string, Image*>("gui_title_d", new Image("gfx/title_d.png")));
    gfx.insert(pair<string, Image*>("gui_title_R", new Image("gfx/title_uppercase_r.png")));
    gfx.insert(pair<string, Image*>("gui_title_y", new Image("gfx/title_y.png")));
    gfx.insert(pair<string, Image*>("gui_title_?", new Image("gfx/title_questionmark.png")));
    gfx.insert(pair<string, Image*>("gui_title_C", new Image("gfx/title_uppercase_c.png")));
    gfx.insert(pair<string, Image*>("gui_title_r", new Image("gfx/title_r.png")));
    gfx.insert(pair<string, Image*>("gui_title_!", new Image("gfx/title_exclamationmark.png")));

    gfx.insert(pair<string, Image*>("gui_title_firework", new Image("gfx/title_firework.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_title_speech_bubble", new Image("gfx/title_speech_bubble.png")));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_play", new Image("gfx/button_main_menu_play.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_extras", new Image("gfx/button_main_menu_extras.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_options", new Image("gfx/button_main_menu_options.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_designer", new Image("gfx/button_main_menu_designer.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_quit", new Image("gfx/button_main_menu_quit.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_main_menu_tutorial", new Image("gfx/button_main_menu_tutorial.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_scroll_button_down", new Image("gfx/scroll_button_down.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_scroll_button_up", new Image("gfx/scroll_button_up.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_scroll_button_down_small", new Image("gfx/scroll_button_down_small.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_scroll_button_up_small", new Image("gfx/scroll_button_up_small.png", False, 4)));

    gfx.insert(pair<string, Image*>("gui_puzzle_grid_background", new Image("gfx/puzzle_grid_background.png", True)));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_white", new Image("gfx/puzzle_cell_white.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_black", new Image("gfx/puzzle_cell_black.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_cell_black_designer", new Image("gfx/puzzle_cell_black_designer.png")));

    gfx.insert(pair<string, Image*>("gui_heart", new Image("gfx/heart.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_verify_status", new Image("gfx/verify_status.png", False, 3)));

    gfx.insert(pair<string, Image*>("gui_button_designer_create", new Image("gfx/button_designer_create.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_edit", new Image("gfx/button_designer_edit.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_delete", new Image("gfx/button_designer_delete.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_down", new Image("gfx/button_designer_move_down.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_move_up", new Image("gfx/button_designer_move_up.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_test", new Image("gfx/button_designer_test.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_save", new Image("gfx/button_designer_save.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_paint", new Image("gfx/button_designer_paint.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_help", new Image("gfx/button_designer_help.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_name", new Image("gfx/button_designer_name.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_size", new Image("gfx/button_designer_size.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_undo", new Image("gfx/button_designer_undo.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_redo", new Image("gfx/button_designer_redo.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_fill", new Image("gfx/button_designer_fill.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_copy", new Image("gfx/button_designer_copy.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_puzzle", new Image("gfx/button_designer_puzzle.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_designer_back", new Image("gfx/button_designer_back.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_designer_throbber", new Image("gfx/designer_throbber.png", False, 10)));

    gfx.insert(pair<string, Image*>("gui_palette_cursor", new Image("gfx/palette_cursor.png")));
    gfx.insert(pair<string, Image*>("gui_value_slider", new Image("gfx/value_slider.png")));

    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_main", new Image("gfx/button_puzzle_type_select_main.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_puzzle_type_select_downloaded", new Image("gfx/button_puzzle_type_select_downloaded.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_go_back", new Image("gfx/button_go_back.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_go_back_small", new Image("gfx/button_go_back_small.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category", new Image("gfx/button_select_category.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category_last", new Image("gfx/button_select_category_last.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_select_category_shadow", new Image("gfx/button_select_category_shadow.png")));
    gfx.insert(pair<string, Image*>("gui_button_select_category_unlock_mask", new Image("gfx/button_select_category_unlock_mask.png")));
    gfx.insert(pair<string, Image*>("gui_category_complete_tick", new Image("gfx/category_complete_tick.png")));
    gfx.insert(pair<string, Image*>("gui_category_complete_star", new Image("gfx/category_complete_star.png")));
    gfx.insert(pair<string, Image*>("gui_category_locked", new Image("gfx/category_locked.png", False, 2)));

    gfx.insert(pair<string, Image*>("gui_button_puzzle_menu", new Image("gfx/button_puzzle_menu.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_menu_button_resume_game", new Image("gfx/menu_button_resume_game.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_menu_button_restart_puzzle", new Image("gfx/menu_button_restart_puzzle.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_menu_button_restart_tutorial", new Image("gfx/menu_button_restart_tutorial.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_menu_button_save_quit", new Image("gfx/menu_button_save_quit.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_menu_button_quit_tutorial", new Image("gfx/menu_button_quit_tutorial.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_menu_button_stop_testing", new Image("gfx/menu_button_stop_testing.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_button_tutorial_next", new Image("gfx/button_tutorial_next.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_tutorial_speech_bubble", new Image("gfx/tutorial_speech_bubble.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_record_clock", new Image("gfx/puzzle_record_clock.png")));

    gfx.insert(pair<string, Image*>("gui_background_present", new Image("gfx/background_present.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_balloons", new Image("gfx/background_balloons.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_designer", new Image("gfx/background_designer.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_tutorial", new Image("gfx/background_tutorial.png", True)));
    gfx.insert(pair<string, Image*>("gui_background_grid", new Image("gfx/background_grid.png", True)));
    gfx.insert(pair<string, Image*>("gui_stars", new Image("gfx/stars.png", True)));
    gfx.insert(pair<string, Image*>("gui_mouse", new Image("gfx/mouse.png")));

    gfx.insert(pair<string, Image*>("gui_puzzle_image_unsolved", new Image("gfx/puzzle_image_unsolved.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_puzzle_box", new Image("gfx/puzzle_select_puzzle_box.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_solved_icon", new Image("gfx/puzzle_select_solved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_saved_icon", new Image("gfx/puzzle_select_saved_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_star_icon", new Image("gfx/puzzle_select_star_icon.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_rating_star", new Image("gfx/puzzle_select_rating_star.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_sharing_rating_stars", new Image("gfx/sharing_rating_stars.png", False, 8)));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_speech_bubble", new Image("gfx/puzzle_select_speech_bubble.png")));
    gfx.insert(pair<string, Image*>("gui_puzzle_select_button_report", new Image("gfx/puzzle_select_button_report.png", False, 4)));

    gfx.insert(pair<string, Image*>("gui_chips_normal", new Image("gfx/chips_normal.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_chips_happy", new Image("gfx/chips_happy.png", False, 2)));
    gfx.insert(pair<string, Image*>("gui_chips_sad", new Image("gfx/chips_sad.png", False, 3)));
    gfx.insert(pair<string, Image*>("gui_speech_bubble", new Image("gfx/speech_bubble.png")));

    gfx.insert(pair<string, Image*>("gui_button_sharing_tab_top_week", new Image("gfx/button_sharing_tab_top_week.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_tab_top", new Image("gfx/button_sharing_tab_top.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_tab_newest", new Image("gfx/button_sharing_tab_newest.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_tab_downloaded", new Image("gfx/button_sharing_tab_downloaded.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_tab_my_puzzles", new Image("gfx/button_sharing_tab_my_puzzles.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_upload", new Image("gfx/button_sharing_upload.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_download", new Image("gfx/button_sharing_download.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_play", new Image("gfx/button_sharing_play.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_delete", new Image("gfx/button_sharing_delete.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_next", new Image("gfx/button_sharing_next.png", False, 4)));
    gfx.insert(pair<string, Image*>("gui_button_sharing_prev", new Image("gfx/button_sharing_prev.png", False, 4)));

    // Sound effects!
    sfx.insert(pair<string,SFX*>("empty_square", new SFX("sfx/empty_square.wav", game, False)));
    sfx.insert(pair<string,SFX*>("fill_square", new SFX("sfx/fill_square.wav", game, False)));
    sfx.insert(pair<string,SFX*>("incorrect_square", new SFX("sfx/incorrect_square.wav", game)));
    sfx.insert(pair<string,SFX*>("success", new SFX("sfx/success.wav", game)));
    sfx.insert(pair<string,SFX*>("failure", new SFX("sfx/failure.wav", game)));
    sfx.insert(pair<string,SFX*>("unlock", new SFX("sfx/unlock.wav", game)));
    sfx.insert(pair<string,SFX*>("button_click", new SFX("sfx/button_click.wav", game)));
    sfx.insert(pair<string,SFX*>("button_hover", new SFX("sfx/button_hover.wav", game)));
    sfx.insert(pair<string,SFX*>("meow1", new SFX("sfx/meow1.wav", game, False)));
    sfx.insert(pair<string,SFX*>("type", new SFX("sfx/type.wav", game)));
    sfx.insert(pair<string,SFX*>("paint", new SFX("sfx/paint.wav", game, False)));
    sfx.insert(pair<string,SFX*>("fill", new SFX("sfx/fill.wav", game)));
    sfx.insert(pair<string,SFX*>("pipette", new SFX("sfx/pipette.wav", game)));
    sfx.insert(pair<string,SFX*>("firework1", new SFX("sfx/firework.wav", game)));
    sfx.insert(pair<string,SFX*>("firework2", new SFX("sfx/firework2.wav", game)));
    sfx.insert(pair<string,SFX*>("firework3", new SFX("sfx/firework3.wav", game)));
    sfx.insert(pair<string,SFX*>("catmode-failure", new SFX("sfx/catmode-failure.wav", game)));
    sfx.insert(pair<string,SFX*>("catmode-empty_square", new SFX("sfx/catmode-empty_square.wav", game, False)));

    // Music
    music.insert(pair<string,Music*>("title", new Music("music/title.ogg", game)));
    music.insert(pair<string,Music*>("select_puzzle", new Music("music/select_puzzle.ogg", game)));
    music.insert(pair<string,Music*>("editor", new Music("music/editor.ogg", game)));
    music.insert(pair<string,Music*>("tutorial", new Music("music/tutorial.ogg", game)));
    music.insert(pair<string,Music*>("puzzle1", new Music("music/puzzle1.ogg", game)));
    music.insert(pair<string,Music*>("puzzle2", new Music("music/puzzle2.ogg", game)));
    music.insert(pair<string,Music*>("puzzle3", new Music("music/puzzle3.ogg", game)));
    music.insert(pair<string,Music*>("puzzle4", new Music("music/puzzle4.ogg", game)));

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

/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app initialisation
 ****************************/

#include <iostream>
using namespace std;
#include "main.h"


 
bool Main_App::On_Init()
{

    // Initialise SDL
    if(SDL_Init(SDL_INIT_EVERYTHING) < 0)
    {
        cout << "Error initialising: " << SDL_GetError() << endl;
        return False;
    }

    if(TTF_Init() < 0)
    {
        cout << "Error initialising font system: " << TTF_GetError() << endl;
        return False;
    }

    if(Mix_OpenAudio(22050, AUDIO_S16SYS, 2, 4096) < 0)
    {
        cout << "Error initialising audio system: " << Mix_GetError() << endl;
#if __LINUX__
        cout << "If using ALSA ensure that the OSS compatability module is loaded." << endl;
#endif
        return False;
    }

    SDL_ShowCursor(SDL_DISABLE);

	SDL_WM_SetCaption("PixelPics", "PixelPics"); 
	SDL_WM_SetIcon(IMG_Load("gfx/prog_icon_32.png"), NULL);

    // create window
    //SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
    //SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 2);
    Uint32 flags = SDL_HWSURFACE | SDL_GL_DOUBLEBUFFER | SDL_OPENGL;

    vector<float> default_screen_res;

    // Get all the allowed screen modes
    SDL_Rect** modes = SDL_ListModes(NULL, SDL_FULLSCREEN|SDL_HWSURFACE);
    for(int i = 0; modes[i]; ++i)
    {
        // Discard anything that's under the lowest allowed res
        if(modes[i]->w < FALLBACK_SCREEN_WIDTH || modes[i]->h < FALLBACK_SCREEN_HEIGHT)
            continue;
        // Discard anything that's an absurd aspect ratio. This is because linux was
        // reporting both monitors together as one big screen. lol
        if((float)modes[i]->w / (float)modes[i]->h > 2.0f)
            continue;

        // Plop the screen list into the allowed screen sizes list
        vector<float> size;
        size.push_back(modes[i]->w); size.push_back(modes[i]->h);
        allowed_screen_sizes.push_back(size);

        // If higher than the current highest default then save it
        if(default_screen_res.size() == 0 || modes[i]->w > default_screen_res[0])
        {
            default_screen_res.empty();
            default_screen_res.push_back(modes[i]->w);
            default_screen_res.push_back(modes[i]->h);
        }
    }

    // If first run this we set the settings to the found default
    if(Main_App::first_run)
    {
        settings->screen_width = default_screen_res[0];
        settings->screen_height = default_screen_res[1];
        settings->save();
    }

    if(settings->full_screen)
        flags |= SDL_FULLSCREEN;

    surf_display = SDL_SetVideoMode(settings->screen_width, settings->screen_height, 32, flags);

    if(surf_display == NULL)
    {

        settings->screen_width = FALLBACK_SCREEN_WIDTH;
        settings->screen_height = FALLBACK_SCREEN_HEIGHT;

        surf_display = SDL_SetVideoMode(settings->screen_width, settings->screen_height, 32, SDL_HWSURFACE | SDL_GL_DOUBLEBUFFER | SDL_OPENGL);
        if(surf_display == NULL)
        {
            cout << "Error initilising video mode."  << endl;
            return False;
        }

    }

	SDL_WM_SetIcon(IMG_Load("gfx/pixelpics.png"), NULL);

    screen_width = settings -> screen_width;
    screen_height = settings -> screen_height;

    // set up opengl context
    glClearColor(0, 0, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT);

    glViewport(0, 0, settings->screen_width, settings->screen_height);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glOrtho(0, settings->screen_width, settings->screen_height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);

    glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    //glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    //glEnable(GL_LINE_SMOOTH);

    // Need this little titbit
    Process::default_texture_coords[0] = 1.0f;
    Process::default_texture_coords[1] = 1.0f;
    Process::default_texture_coords[3] = 1.0f;
    Process::default_texture_coords[4] = 1.0f;

    // Create the mouse
    mouse = new Mouse();

    // Load all the media
    Main_App::media = new Media(this);

    // Start up python
    python_interface = new Python_Interface(this);
    if(!python_interface -> initialise_python_interpreter())
        return False;

    // Set up process draw strategies
    draw_strategies["primitive_square"] = &Process::Draw_strategy_primitive_square;
    draw_strategies["primitive_line"] = &Process::Draw_strategy_primitive_line;
    draw_strategies["gui_button"] = &Process::Draw_strategy_gui_button;
    draw_strategies["gui_window_frame"] = &Process::Draw_strategy_gui_window_frame;
    draw_strategies["gui_text_input"] = &Process::Draw_strategy_gui_text_input;
    draw_strategies["gui_dropdown_currently_selected"] = &Process::Draw_strategy_gui_dropdown_currently_selected;
    draw_strategies["gui_dropdown_options"] = &Process::Draw_strategy_gui_dropdown_options;
    draw_strategies["gui_scroll_window"] = &Process::Draw_strategy_gui_scroll_window;
    draw_strategies["puzzle"] = &Process::Draw_strategy_puzzle;
    draw_strategies["puzzle_pixel_message"] = &Process::Draw_strategy_puzzle_pixel_message;
    draw_strategies["gui_designer_packs_pack_item"] = &Process::Draw_strategy_gui_designer_packs_pack_item;
    draw_strategies["gui_spinner"] = &Process::Draw_strategy_gui_spinner;
    draw_strategies["gui_slider"] = &Process::Draw_strategy_gui_slider;
    draw_strategies["gui_designer_designer_menu_bar"] = &Process::Draw_strategy_gui_designer_designer_menu_bar;
    draw_strategies["gui_designer_monochrome_puzzle_image"] = &Process::Draw_strategy_gui_designer_monochrome_puzzle_image;
    draw_strategies["designer_puzzle_background_item"] = &Process::Draw_strategy_designer_puzzle_background_item;
    draw_strategies["designer_colour_current_colour"] = &Process::Draw_strategy_designer_colour_current_colour;
    draw_strategies["designer_colour_value_slider"] = &Process::Draw_strategy_designer_colour_value_slider;
    draw_strategies["balloons_background"] = &Process::Draw_strategy_balloons_background;
    draw_strategies["tutorial_background"] = &Process::Draw_strategy_tutorial_background;
    draw_strategies["designer_background"] = &Process::Draw_strategy_designer_background;
    draw_strategies["present_background"] = &Process::Draw_strategy_present_background;
    draw_strategies["puzzle_select"] = &Process::Draw_strategy_puzzle_select;
    draw_strategies["puzzle_select_puzzle_item"] = &Process::Draw_strategy_puzzle_select_puzzle_item;
    draw_strategies["main_menu_title"] = &Process::Draw_strategy_main_menu_title;

    return True;

}


/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app Header
 ****************************/

#ifndef _MAIN_H_
#define _MAIN_H_

#define BOOST_PYTHON_STATIC_LIB

// Compatibility settings
// lololol microsoft on the GL_BGR thing
#if _WIN32
#include <windows.h>
#include <Shlobj.h>
#include <string>

#ifndef GL_BGR
#define GL_BGR GL_BGR_EXT
#endif
#ifndef GL_BGRA
#define GL_BGRA GL_BGRA_EXT
#endif

#define SEPARATOR "\\"

#else 

#define SEPARATOR "/"

#endif

// Yeah so what?
#define True true
#define False false

// Default settings
#define DEFAULT_SETTING_SCREEN_WIDTH 1024
#define DEFAULT_SETTING_SCREEN_HEIGHT 768
#define DEFAULT_SETTING_FULL_SCREEN "0"
#define DEFAULT_SETTING_SOUND_EFFECTS_ON "1"
#define DEFAULT_SETTING_MUSIC_ON "1"
#define DEFAULT_SETTING_SOUND_EFFECTS_VOL "100"
#define DEFAULT_SETTING_MUSIC_VOL "100"
#define DEFAULT_SETTING_MOUSE_LEFT_EMPTY "1"
#define DEFAULT_SETTING_BUMP_SCROLL "1"
#define DEFAULT_SETTING_LOCK_DRAWING "1"

// Misc defines
#define FILE_SETTINGS "settings.json"
#define FILE_PACK_INFO_FILE "pack.dat"
#define FILE_PUZZLE_EXTENSION ".puz"
#define FILE_SAVES_EXTENSION ".sav"
#define FILE_USER_PACK_DIRECTORY "packs"
#define FILE_GAME_PACK_DIRECTORY "packs"
#define FILE_AUTHOR_ID_FILE "author_id.dat"
#define FILE_PLAYER_PROGRESS "player.dat"
#define FILE_SAVES_DIRECTORY "saves"
#define FILE_SAVES_GAME_DIRECTORY "game"
#define FILE_SAVES_USER_DIRECTORY "user"
#define MAX_PUZZLES_PER_PACK 20
#define MIN_PUZZLE_SIZE 5
#define MAX_PUZZLE_SIZE 40
#define PUZZLE_CELL_WIDTH 64
#define PUZZLE_CELL_HEIGHT 64
#define PUZZLE_HINT_GRADIENT_WIDTH 300.0
#define PUZZLE_RENDER_CHUNK_SIZE 10
#define PUZZLE_UNLOCK_THRESHOLD 15

// STD and boost includes
#include <vector>
#include <iostream>
#include <fstream>
#include <math.h>
#include "boost/foreach.hpp"
#include "boost/tuple/tuple.hpp"
#include "boost/format.hpp"
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/string_generator.hpp>
#include <boost/uuid/random_generator.hpp>

// GL and SDL
#include <GL/gl.h>
#include <GL/glu.h>
#include <SDL/SDL.h>
#include <SDL/SDL_timer.h>
#include <SDL/SDL_ttf.h>

// Program includes
#include "image.h"
#include "font.h"
#include "process.h"
#include "media.h"
#include "game_objects.h"
#include "python_interface.h"

extern Uint32 SDL_RMASK;
extern Uint32 SDL_GMASK;
extern Uint32 SDL_BMASK;
extern Uint32 SDL_AMASK;


class Mouse;
class Settings;


/*
 */
class Main_App
{
 
private:
    bool running;
    SDL_Surface* surf_display;
    int desired_fps;
    int delay_ticks;
    int frames_rendered;
    int time_taken_this_frame;
    Python_Interface* python_interface;

    void Wait_till_next_frame();


public:
    typedef void (Process::*FuncGetter)();
    static map <string, FuncGetter> draw_strategies;

    static float screen_width;
    static float screen_height;

    Settings* settings;
    Media* media;
    std::vector<SDLKey> Keyboard_keys_down;
    std::vector<SDLKey> Keyboard_keys_released;
    std::vector<int> Text_input;
    int current_fps;
    int process_count;
    bool text_input_enabled;
    string path_application_data;
    string path_settings_file;
    string path_user_pack_directory;
    string path_game_pack_directory;
    string path_saves_directory;
    string path_saves_game_directory;
    string path_saves_user_directory;
    string path_author_id_file;
    string path_player_progress;
    string author_id;

    Mouse* mouse;

    vector< vector<float> > allowed_screen_sizes;

    static void putpixel(SDL_Surface *surface, int x, int y, Uint32 pixel);
    static void HSVtoRGB(float h, float s, float v, vector<int> *pixel);
    tuple<int, int, int> PyHSVtoRGB(float h, float s, float v);

    Main_App();
    void Quit();
    int On_Execute();
    bool On_Init();   
    void On_Event(SDL_Event* Event);    
    void On_Loop();    
    void On_Render();    
    void Do_Process_Clean();
    void On_Cleanup(); 
    bool Keyboard_key_down(SDLKey Key);
    bool Keyboard_key_released(SDLKey Key);
    void Toggle_text_input();

};


/*
 */
class Mouse
{
public:
    float x;
    float y;
    float x_rel;
    float y_rel;
    bool left_down;
    bool left_up;
    bool right_down;
    bool right_up;
    bool middle_down;
    bool middle_up;
    bool wheel_down;
    bool wheel_up;

    void set_pos(int x_pos, int y_pos);
};


/*
 */
class Settings
{
public:
    Settings();
    Settings(string _filename);

    string filename;
    float screen_width;
    float screen_height;
    bool full_screen;
    bool sound_effects_on;
    bool music_on;
    int sound_effects_vol;
    int music_vol;
    bool mouse_left_empty;
    bool bump_scroll;
    bool lock_drawing;

    bool save();
};


bool hasattr(boost::python::object obj, std::string const &attr_name);


#endif

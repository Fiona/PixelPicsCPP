/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Handles all the python interfacing code
 ****************************/

#include <iostream>
using namespace std;
#include "main.h"


using namespace boost::python;

namespace my
{

    boost::python::object tuple_to_python(boost::tuples::null_type)
    {
        return boost::python::tuple();
    }

    template <class H, class T>
    boost::python::object tuple_to_python(boost::tuples::cons<H,T> const& x)
    {
        return boost::python::make_tuple(x.get_head()) + my::tuple_to_python(x.get_tail());
    }

    template <class T>
    struct tupleconverter
    {
        static PyObject* convert(T const& x)
        {
            return incref(my::tuple_to_python(x).ptr());
        }
    };

}


/*
 * This is the code that creates the game_core module.
 * It exposes all the objects and methods that Python needs
 * to be able to access.
 */
BOOST_PYTHON_MODULE(core)
{

    typedef boost::tuples::tuple<float, float> screen_pos_tuple;
    to_python_converter<screen_pos_tuple, my::tupleconverter<screen_pos_tuple> >();

    typedef boost::tuples::tuple<int, int, int> three_int_moon_shirt;
    to_python_converter<three_int_moon_shirt, my::tupleconverter<three_int_moon_shirt> >();
    
    // Expose all media related objects
    class_<Image>("Image")
        .def_readonly("num_of_frames", &Image::num_of_frames)
        .def_readonly("width", &Image::width)
        .def_readonly("height", &Image::height)
        ;
    class_<Font>("Font");
    class_<SFX>("SFX")
        .def("play", &SFX::play)
        .def("stop", &SFX::stop)
        ;
    class_<Music>("Music")
        .def("play_loop", &Music::play_loop)
        .def("play", &Music::play)
        .def("stop", &Music::stop)
        .def("set_volume", &Music::set_volume)
        ;

    STL_MAP_WRAPPING_PTR(string, Image*, "gfxMap");
    STL_MAP_WRAPPING_PTR(string, Font*, "fontMap");
    STL_MAP_WRAPPING_PTR(string, SFX*, "sfxMap");
    STL_MAP_WRAPPING_PTR(string, Music*, "musicMap");
    class_<Media>("Media")
        .def_readonly("gfx", &Media::gfx)
        .def_readonly("fonts", &Media::fonts)
        .def_readonly("sfx", &Media::sfx)
        .def_readonly("music", &Media::music)
        ;

    // Expose settings object
    class_<Settings>("Settings")
        .add_property("screen_width", make_getter(&Settings::screen_width), make_setter(&Settings::screen_width))
        .add_property("screen_height", make_getter(&Settings::screen_height), make_setter(&Settings::screen_height))
        .add_property("full_screen", make_getter(&Settings::full_screen), make_setter(&Settings::full_screen))
        .add_property("music_on", make_getter(&Settings::music_on), make_setter(&Settings::music_on))
        .add_property("sound_effects_on", make_getter(&Settings::sound_effects_on), make_setter(&Settings::sound_effects_on))
        .add_property("music_vol", make_getter(&Settings::music_vol), make_setter(&Settings::music_vol))
        .add_property("sound_effects_vol", make_getter(&Settings::sound_effects_vol), make_setter(&Settings::sound_effects_vol))
        .add_property("mouse_left_empty", make_getter(&Settings::mouse_left_empty), make_setter(&Settings::mouse_left_empty))
        .add_property("bump_scroll", make_getter(&Settings::bump_scroll), make_setter(&Settings::bump_scroll))
        .add_property("lock_drawing", make_getter(&Settings::lock_drawing), make_setter(&Settings::lock_drawing))
        .add_property("cat_mode", make_getter(&Settings::cat_mode), make_setter(&Settings::cat_mode))
        .def("save", &Settings::save)
        ;

    // Expose common vectors
    boost::python::class_<std::vector<float> >("FloatVector")
        .def(boost::python::vector_indexing_suite<std::vector<float> >());
    boost::python::class_<std::vector<int> >("IntVector")
        .def(boost::python::vector_indexing_suite<std::vector<int> >());
    boost::python::class_<std::vector< std::vector<float> > >("FloatVectorVector")
        .def(boost::python::vector_indexing_suite<std::vector< std::vector<float> > >());

    // Expose Process object
    class_<Process, ProcessWrapper, boost::noncopyable, boost::shared_ptr<ProcessWrapper> >("Process", init<>())
        .def("Execute", &Process::Execute, &ProcessWrapper::Execute_default)
        .def("On_Exit", &Process::On_Exit, &ProcessWrapper::On_Exit_default)
        .def("get_screen_draw_position", &Process::get_screen_draw_position, &ProcessWrapper::get_screen_draw_position_default)

        .add_property("x", make_getter(&Process::x), make_setter(&Process::x))
        .add_property("y", make_getter(&Process::y), make_setter(&Process::y))
        .add_property("z", make_getter(&Process::z), &Process::Set_z)
        .add_property("priority", make_getter(&Process::priority), &Process::Set_priority)
        .add_property("colour", make_getter(&Process::colour), &Process::Set_colour)
        .add_property("clip", make_getter(&Process::clip), &Process::Set_clip)
        .add_property("alpha", make_getter(&Process::alpha), make_setter(&Process::alpha))
        .add_property("scale", make_getter(&Process::scale), make_setter(&Process::scale))
        .add_property("rotation", make_getter(&Process::rotation), make_setter(&Process::rotation))
        .add_property("image_sequence", make_getter(&Process::image_sequence), make_setter(&Process::image_sequence))
        .add_property("scale_pos", make_getter(&Process::scale_pos), &Process::Set_scale_pos)
        .add_property("draw_strategy", make_getter(&Process::draw_strategy), make_setter(&Process::draw_strategy))

        .add_property(
            "image",
            make_getter(&Process::image, return_value_policy<reference_existing_object>()),
            make_setter(&Process::image)
            )

        .def("move_forward", &Process::move_forward)
        .def("Kill", &ProcessWrapper::Kill)
        .def("create_image_from_puzzle", &Process::create_image_from_puzzle)
        .def("destroy_puzzle_image", &Process::destroy_puzzle_image)
        .def("create_image_as_pallete", &Process::create_image_as_pallete)
        ;

    // Expose Text object
    class_<Text, TextWrapper, boost::noncopyable, boost::shared_ptr<TextWrapper> >("Text", init< Font*, float, float, int, string >())
        .add_property(
            "text",
            make_getter(&Text::text),
            &Text::set_text
            )
        .add_property("x", make_getter(&Text::x), make_setter(&Text::x))
        .add_property("y", make_getter(&Text::y), make_setter(&Text::y))
        .add_property("z", make_getter(&Text::z), &Text::Set_z)
        .add_property("alpha", make_getter(&Text::alpha), make_setter(&Text::alpha))
        .add_property("scale", make_getter(&Text::scale), make_setter(&Text::scale))
        .add_property("rotation", make_getter(&Text::rotation), make_setter(&Text::rotation))
        .add_property("colour", make_getter(&Text::colour), &Text::Set_colour)
        .add_property("clip", make_getter(&Text::clip), &Text::Set_clip)
        .add_property("shadow", make_getter(&Text::shadow), make_setter(&Text::shadow))
        .add_property("shadow_colour", make_getter(&Text::shadow_colour), &Text::Set_shadow_colour)
        .add_property("text_width", make_getter(&Text::text_width), make_setter(&Text::text_width))
        .add_property("text_height", make_getter(&Text::text_height), make_setter(&Text::text_height))
        .add_property("generate_mipmaps", make_getter(&Text::generate_mipmaps), &Text::Set_generate_mipmaps)
        .def("Kill", &TextWrapper::Kill)
        ;

    // Expose the mouse class
    class_<Mouse>("Mouse")
        .add_property("x", make_getter(&Mouse::x))
        .add_property("y", make_getter(&Mouse::y))
        .add_property("x_rel", make_getter(&Mouse::x_rel))
        .add_property("y_rel", make_getter(&Mouse::y_rel))
        .add_property("left_down", make_getter(&Mouse::left_down))
        .add_property("left_up", make_getter(&Mouse::left_up))
        .add_property("right_down", make_getter(&Mouse::right_down))
        .add_property("right_up", make_getter(&Mouse::right_up))
        .add_property("middle_down", make_getter(&Mouse::middle_down))
        .add_property("middle_up", make_getter(&Mouse::middle_up))
        .add_property("wheel_down", make_getter(&Mouse::wheel_down))
        .add_property("wheel_up", make_getter(&Mouse::wheel_up))
        .def("set_pos", &Mouse::set_pos)
        ;

    // Expose the main app obj
    class_<Main_App>("Main_App")
        .add_property("mouse", make_getter(&Main_App::mouse, return_value_policy<reference_existing_object>()))
        .add_property("current_fps", make_getter(&Main_App::current_fps))
        .add_property("process_count", make_getter(&Main_App::process_count))
        .add_property("text_input_enabled", make_getter(&Main_App::text_input_enabled), make_setter(&Main_App::text_input_enabled))
        .add_property("Text_input", make_getter(&Main_App::Text_input))
        .add_static_property("media", make_getter(&Main_App::media, return_value_policy<reference_existing_object>()))
        //.add_property("media", make_getter(&Main_App::media, return_value_policy<reference_existing_object>()))
        .add_property("settings", make_getter(&Main_App::settings, return_value_policy<reference_existing_object>()))
        .add_property("author_id", make_getter(&Main_App::author_id))
        .add_property("path_application_data", make_getter(&Main_App::path_application_data))
        .add_property("path_settings_file", make_getter(&Main_App::path_settings_file))
        .add_property("path_user_pack_directory", make_getter(&Main_App::path_user_pack_directory))
        .add_property("path_game_pack_directory", make_getter(&Main_App::path_game_pack_directory))
        .add_property("path_player_progress", make_getter(&Main_App::path_player_progress))
        .add_property("path_saves_directory", make_getter(&Main_App::path_saves_directory))
        .add_property("path_saves_game_directory", make_getter(&Main_App::path_saves_game_directory))
        .add_property("path_saves_user_directory", make_getter(&Main_App::path_saves_user_directory))
        .add_property("allowed_screen_sizes", make_getter(&Main_App::allowed_screen_sizes))
        .def("Keyboard_key_down", &Main_App::Keyboard_key_down)
        .def("Keyboard_key_released", &Main_App::Keyboard_key_released)
        .def("Toggle_text_input", &Main_App::Toggle_text_input)
        .def("Quit", &Main_App::Quit)
        .def("HSVtoRGB", &Main_App::PyHSVtoRGB)
        .def("Is_music_playing", &Main_App::Is_music_playing)
        ;

    // Used for outputting debugging
#ifdef DEBUG
    scope().attr("DEBUG") = true;
    scope().attr("SHARING_ADDRESS") = LOCAL_SHARING_ADDRESS;
#else
    scope().attr("DEBUG") = false;
    scope().attr("SHARING_ADDRESS") = REMOTE_SHARING_ADDRESS;
#endif

    // Demo mode
#ifdef DEMO
    scope().attr("DEMO") = true;
#else
    scope().attr("DEMO") = false;
#endif

    scope().attr("VERSION") = VERSION;

    // Expose the framework constants
    scope().attr("TEXT_ALIGN_TOP_LEFT") = TEXT_ALIGN_TOP_LEFT;
    scope().attr("TEXT_ALIGN_TOP") = TEXT_ALIGN_TOP;
    scope().attr("TEXT_ALIGN_TOP_RIGHT") = TEXT_ALIGN_TOP_RIGHT;
    scope().attr("TEXT_ALIGN_CENTER_LEFT") = TEXT_ALIGN_CENTER_LEFT;
    scope().attr("TEXT_ALIGN_CENTER") = TEXT_ALIGN_CENTER;
    scope().attr("TEXT_ALIGN_CENTER_RIGHT") = TEXT_ALIGN_CENTER_RIGHT;
    scope().attr("TEXT_ALIGN_BOTTOM_LEFT") = TEXT_ALIGN_BOTTOM_LEFT;
    scope().attr("TEXT_ALIGN_BOTTOM") = TEXT_ALIGN_BOTTOM;
    scope().attr("TEXT_ALIGN_BOTTOM_RIGHT") = TEXT_ALIGN_BOTTOM_RIGHT;

    // Expose some pixelpics constants
    scope().attr("FILE_PACK_INFO_FILE") = FILE_PACK_INFO_FILE;
    scope().attr("FILE_PUZZLE_EXTENSION") = FILE_PUZZLE_EXTENSION;
    scope().attr("FILE_SAVES_EXTENSION") = FILE_SAVES_EXTENSION;
    scope().attr("FILE_PLAYER_PROGRESS") = FILE_PLAYER_PROGRESS;
    scope().attr("MAX_PUZZLES_PER_PACK") = MAX_PUZZLES_PER_PACK;
    scope().attr("MIN_PUZZLE_SIZE") = MIN_PUZZLE_SIZE;
    scope().attr("MAX_PUZZLE_SIZE") = MAX_PUZZLE_SIZE;
    scope().attr("PUZZLE_CELL_WIDTH") = PUZZLE_CELL_WIDTH;
    scope().attr("PUZZLE_CELL_HEIGHT") = PUZZLE_CELL_HEIGHT;
    scope().attr("PUZZLE_HINT_GRADIENT_WIDTH") = PUZZLE_HINT_GRADIENT_WIDTH;
    scope().attr("PUZZLE_RENDER_CHUNK_SIZE") = PUZZLE_RENDER_CHUNK_SIZE;
    scope().attr("PUZZLE_UNLOCK_THRESHOLD") = PUZZLE_UNLOCK_THRESHOLD;
    scope().attr("BUMP_SCROLL_BORDER_WIDTH") = BUMP_SCROLL_BORDER_WIDTH;
    scope().attr("BUMP_SCROLL_SPEED") = BUMP_SCROLL_SPEED;

    // Expose all the SDL Keybinding constants
    enum_<SDLKey>("key")
        // Ascii keys
        .value("UNKNOWN", SDLK_UNKNOWN)
        .value("FIRST", SDLK_FIRST)
        .value("BACKSPACE", SDLK_BACKSPACE)
        .value("TAB", SDLK_TAB)
        .value("CLEAR", SDLK_CLEAR)
        .value("RETURN", SDLK_RETURN)
        .value("PAUSE", SDLK_PAUSE)
        .value("ESCAPE",SDLK_ESCAPE) 
        .value("SPACE", SDLK_SPACE)
        .value("EXCLAIM", SDLK_EXCLAIM)
        .value("QUOTEDBL", SDLK_QUOTEDBL)
        .value("HASH", SDLK_HASH)
        .value("DOLLAR", SDLK_DOLLAR)
        .value("AMPERSAND", SDLK_AMPERSAND)
        .value("QUOTE", SDLK_QUOTE)
        .value("LEFTPAREN", SDLK_LEFTPAREN)
        .value("RIGHTPAREN", SDLK_RIGHTPAREN)
        .value("ASTERISK", SDLK_ASTERISK)
        .value("PLUS", SDLK_PLUS)
        .value("COMMA", SDLK_COMMA)
        .value("MINUS", SDLK_MINUS)
        .value("PERIOD", SDLK_PERIOD)
        .value("SLASH", SDLK_SLASH)
        .value("0", SDLK_0)
        .value("1", SDLK_1)
        .value("2", SDLK_2)
        .value("3", SDLK_3)
        .value("4", SDLK_4)
        .value("5", SDLK_5)
        .value("6", SDLK_6)
        .value("7", SDLK_7)
        .value("8", SDLK_8)
        .value("9", SDLK_9)
        .value("COLON", SDLK_COLON)
        .value("SEMICOLON", SDLK_SEMICOLON)
        .value("LESS", SDLK_LESS)
        .value("EQUALS", SDLK_EQUALS)
        .value("GREATER", SDLK_GREATER)
        .value("QUESTION", SDLK_QUESTION)
        .value("AT", SDLK_AT)

        // (Skip uppercase letters)
        .value("LEFTBRACKET", SDLK_LEFTBRACKET)
        .value("BACKSLASH", SDLK_BACKSLASH)
        .value("RIGHTBRACKET", SDLK_RIGHTBRACKET)
        .value("CARET", SDLK_CARET)
        .value("UNDERSCORE", SDLK_UNDERSCORE)
        .value("BACKQUOTE", SDLK_BACKQUOTE)
        .value("a", SDLK_a)
        .value("b", SDLK_b)
        .value("c", SDLK_c)
        .value("d", SDLK_d)
        .value("e", SDLK_e)
        .value("f", SDLK_f)
        .value("g", SDLK_g)
        .value("h", SDLK_h)
        .value("i", SDLK_i)
        .value("j", SDLK_j)
        .value("k", SDLK_k)
        .value("l", SDLK_l)
        .value("m", SDLK_m)
        .value("n", SDLK_n)
        .value("o", SDLK_o)
        .value("p", SDLK_p)
        .value("q", SDLK_q)
        .value("r", SDLK_r)
        .value("s", SDLK_s)
        .value("t", SDLK_t)
        .value("u", SDLK_u)
        .value("v", SDLK_v)
        .value("w", SDLK_w)
        .value("x", SDLK_x)
        .value("y", SDLK_y)
        .value("z", SDLK_z)
        .value("DELETE", SDLK_DELETE)
        // End of ASCII keys

        // International keyboard syms
        .value("WORLD_0", SDLK_WORLD_0)
        .value("WORLD_1", SDLK_WORLD_1)
        .value("WORLD_2", SDLK_WORLD_2)
        .value("WORLD_3", SDLK_WORLD_3)
        .value("WORLD_4", SDLK_WORLD_4)
        .value("WORLD_5", SDLK_WORLD_5)
        .value("WORLD_6", SDLK_WORLD_6)
        .value("WORLD_7", SDLK_WORLD_7)
        .value("WORLD_8", SDLK_WORLD_8)
        .value("WORLD_9", SDLK_WORLD_9)
        .value("WORLD_10", SDLK_WORLD_10)
        .value("WORLD_11", SDLK_WORLD_11)
        .value("WORLD_12", SDLK_WORLD_12)
        .value("WORLD_13", SDLK_WORLD_13)
        .value("WORLD_14", SDLK_WORLD_14)
        .value("WORLD_15", SDLK_WORLD_15)
        .value("WORLD_16", SDLK_WORLD_16)
        .value("WORLD_17", SDLK_WORLD_17)
        .value("WORLD_18", SDLK_WORLD_18)
        .value("WORLD_19", SDLK_WORLD_19)
        .value("WORLD_20", SDLK_WORLD_20)
        .value("WORLD_21", SDLK_WORLD_21)
        .value("WORLD_22", SDLK_WORLD_22)
        .value("WORLD_23", SDLK_WORLD_23)
        .value("WORLD_24", SDLK_WORLD_24)
        .value("WORLD_25", SDLK_WORLD_25)
        .value("WORLD_26", SDLK_WORLD_26)
        .value("WORLD_27", SDLK_WORLD_27)
        .value("WORLD_28", SDLK_WORLD_28)
        .value("WORLD_29", SDLK_WORLD_29)
        .value("WORLD_30", SDLK_WORLD_30)
        .value("WORLD_31", SDLK_WORLD_31)
        .value("WORLD_32", SDLK_WORLD_32)
        .value("WORLD_33", SDLK_WORLD_33)
        .value("WORLD_34", SDLK_WORLD_34)
        .value("WORLD_35", SDLK_WORLD_35)
        .value("WORLD_36", SDLK_WORLD_36)
        .value("WORLD_37", SDLK_WORLD_37)
        .value("WORLD_38", SDLK_WORLD_38)
        .value("WORLD_39", SDLK_WORLD_39)
        .value("WORLD_40", SDLK_WORLD_40)
        .value("WORLD_41", SDLK_WORLD_41)
        .value("WORLD_42", SDLK_WORLD_42)
        .value("WORLD_43", SDLK_WORLD_43)
        .value("WORLD_44", SDLK_WORLD_44)
        .value("WORLD_45", SDLK_WORLD_45)
        .value("WORLD_46", SDLK_WORLD_46)
        .value("WORLD_47", SDLK_WORLD_47)
        .value("WORLD_48", SDLK_WORLD_48)
        .value("WORLD_49", SDLK_WORLD_49)
        .value("WORLD_50", SDLK_WORLD_50)
        .value("WORLD_51", SDLK_WORLD_51)
        .value("WORLD_52", SDLK_WORLD_52)
        .value("WORLD_53", SDLK_WORLD_53)
        .value("WORLD_54", SDLK_WORLD_54)
        .value("WORLD_55", SDLK_WORLD_55)
        .value("WORLD_56", SDLK_WORLD_56)
        .value("WORLD_57", SDLK_WORLD_57)
        .value("WORLD_58", SDLK_WORLD_58)
        .value("WORLD_59", SDLK_WORLD_59)
        .value("WORLD_60", SDLK_WORLD_60)
        .value("WORLD_61", SDLK_WORLD_61)
        .value("WORLD_62", SDLK_WORLD_62)
        .value("WORLD_63", SDLK_WORLD_63)
        .value("WORLD_64", SDLK_WORLD_64)
        .value("WORLD_65", SDLK_WORLD_65)
        .value("WORLD_66", SDLK_WORLD_66)
        .value("WORLD_67", SDLK_WORLD_67)
        .value("WORLD_68", SDLK_WORLD_68)
        .value("WORLD_69", SDLK_WORLD_69)
        .value("WORLD_70", SDLK_WORLD_70)
        .value("WORLD_71", SDLK_WORLD_71)
        .value("WORLD_72", SDLK_WORLD_72)
        .value("WORLD_73", SDLK_WORLD_73)
        .value("WORLD_74", SDLK_WORLD_74)
        .value("WORLD_75", SDLK_WORLD_75)
        .value("WORLD_76", SDLK_WORLD_76)
        .value("WORLD_77", SDLK_WORLD_77)
        .value("WORLD_78", SDLK_WORLD_78)
        .value("WORLD_79", SDLK_WORLD_79)
        .value("WORLD_80", SDLK_WORLD_80)
        .value("WORLD_81", SDLK_WORLD_81)
        .value("WORLD_82", SDLK_WORLD_82)
        .value("WORLD_83", SDLK_WORLD_83)
        .value("WORLD_84", SDLK_WORLD_84)
        .value("WORLD_85", SDLK_WORLD_85)
        .value("WORLD_86", SDLK_WORLD_86)
        .value("WORLD_87", SDLK_WORLD_87)
        .value("WORLD_88", SDLK_WORLD_88)
        .value("WORLD_89", SDLK_WORLD_89)
        .value("WORLD_90", SDLK_WORLD_90)
        .value("WORLD_91", SDLK_WORLD_91)
        .value("WORLD_92", SDLK_WORLD_92)
        .value("WORLD_93", SDLK_WORLD_93)
        .value("WORLD_94", SDLK_WORLD_94)
        .value("WORLD_95", SDLK_WORLD_95)

        // Numpad
        .value("KP0", SDLK_KP0)
        .value("KP1", SDLK_KP1)
        .value("KP2", SDLK_KP2)
        .value("KP3", SDLK_KP3)
        .value("KP4", SDLK_KP4)
        .value("KP5", SDLK_KP5)
        .value("KP6", SDLK_KP6)
        .value("KP7", SDLK_KP7)
        .value("KP8", SDLK_KP8)
        .value("KP9", SDLK_KP9)
        .value("KP_PERIOD", SDLK_KP_PERIOD)
        .value("KP_DIVIDE", SDLK_KP_DIVIDE)
        .value("KP_MULTIPLY", SDLK_KP_MULTIPLY)
        .value("KP_MINUS", SDLK_KP_MINUS)
        .value("KP_PLUS", SDLK_KP_PLUS)
        .value("KP_ENTER", SDLK_KP_ENTER)
        .value("KP_EQUALS", SDLK_KP_EQUALS)

        // Home/end pad and arrows
        .value("UP", SDLK_UP)
        .value("DOWN", SDLK_DOWN)
        .value("RIGHT", SDLK_RIGHT)
        .value("LEFT", SDLK_LEFT)
        .value("INSERT", SDLK_INSERT)
        .value("HOME", SDLK_HOME)
        .value("END", SDLK_END)
        .value("PAGEUP", SDLK_PAGEUP)
        .value("PAGEDOWN", SDLK_PAGEDOWN)

        // Function keys
        .value("F1", SDLK_F1)
        .value("F2", SDLK_F2)
        .value("F3", SDLK_F3)
        .value("F4", SDLK_F4)
        .value("F5", SDLK_F5)
        .value("F6", SDLK_F6)
        .value("F7", SDLK_F7)
        .value("F8", SDLK_F8)
        .value("F9", SDLK_F9)
        .value("F10", SDLK_F10)
        .value("F11", SDLK_F11)
        .value("F12", SDLK_F12)
        .value("F13", SDLK_F13)
        .value("F14", SDLK_F14)
        .value("F15", SDLK_F15)

        // Key modifiers
        .value("NUMLOCK", SDLK_NUMLOCK)
        .value("CAPSLOCK", SDLK_CAPSLOCK)
        .value("SCROLLOCK", SDLK_SCROLLOCK)
        .value("RSHIFT", SDLK_RSHIFT)
        .value("LSHIFT", SDLK_LSHIFT)
        .value("RCTRL", SDLK_RCTRL)
        .value("LCTRL", SDLK_LCTRL)
        .value("RALT", SDLK_RALT)
        .value("LALT", SDLK_LALT)
        .value("RMETA", SDLK_RMETA)
        .value("LMETA", SDLK_LMETA)
        .value("LSUPER", SDLK_LSUPER)            // Left "Windows" key
        .value("RSUPER", SDLK_RSUPER)            // Right "Windows" key
        .value("MODE", SDLK_MODE)                // "Alt Gr" key 
        .value("COMPOSE", SDLK_COMPOSE)          // Multi-key compose key

        /// Miscellaneous function keys
        .value("HELP", SDLK_HELP)
        .value("PRINT", SDLK_PRINT)
        .value("SYSREQ", SDLK_SYSREQ)
        .value("BREAK", SDLK_BREAK)
        .value("MENU", SDLK_MENU)
        .value("POWER", SDLK_POWER)             // Power Macintosh power key 
        .value("EURO", SDLK_EURO)               // Some european keyboards
        .value("UNDO", SDLK_UNDO)               // Atari keyboard has Undo

        .export_values()
        ;

}

/*
 * Constructor
 *
 * @param Main_App* game Reference to the main application instance.
 */
Python_Interface::Python_Interface(Main_App* _game)
{
    game = _game;
}


/*
 * Starts up the python interpreter, creates the default
 * namespace and runs the main script.
 * 
 * @returns bool If an error was spit out by the python interpreter upon init.
 */
bool Python_Interface::initialise_python_interpreter()
{

    try
    {

#if __WIN32__
        PyRun_SimpleString("import cStringIO");
        PyRun_SimpleString("import sys");
        PyRun_SimpleString("sys.stderr = cStringIO.StringIO()");
#endif

        object main_module = import("__main__");
        object main_namespace = main_module.attr("__dict__");

        initcore();

		main_namespace["core"] = ptr(game);

        PyObject* sysPath = PySys_GetObject((char*)"path");
        std::string paths;
        std::string module_path;

#if defined(_M_IX86) || defined(__i386__)
        module_path = "'python27/i386'";
#else
        module_path = "'python27/x86_64'";
#endif

#ifdef DEBUG
        // In debug we load code from a source directory
        paths = "sys.path += ['logic']\n";
#else
        // In release we load code and std library from zip files
        paths = "sys.path = ['logic.dat', 'python27/python27.zip', 'python27/python27.zip/plat-linux2', 'python27/python27.zip/lib-tk', 'python27/python27.zip/lib-old', 'python27', " + module_path + "]\n";
#endif

        // Bootstrap the main game object and start it
        std::string code = std::string("import sys\n") +
            paths +
            "from core import *\n" +
            "from main import *\n" +
            "Game(core)\n";
        object ignored = exec(
            boost::python::str(code),
            main_namespace,
			main_namespace
            );

    }
    catch(error_already_set const &)
    {

        PyErr_Print();

#if __WIN32__
        boost::python::object sys(
            boost::python::handle<>(PyImport_ImportModule("sys"))
        );
        boost::python::object err = sys.attr("stderr");
        std::string err_text = boost::python::extract<std::string>(err.attr("getvalue")());
        MessageBox(0, err_text.c_str(), "Python Error", MB_OK);
#endif

        return False;

    }

    return True;

}

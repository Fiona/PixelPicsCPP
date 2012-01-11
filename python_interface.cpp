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


/*
 * This is the code that creates the game_core module.
 * It exposes all the objects and methods that Python needs
 * to be able to access.
 */
BOOST_PYTHON_MODULE(game_core)
{
    
    // Expose all media related objects
    class_<Image>("Image");
    class_<Font>("Font");

    STL_MAP_WRAPPING_PTR(string, Image*, "gfxMap");
    STL_MAP_WRAPPING_PTR(string, Font*, "fontMap");
    class_<Media>("Media")
        .def_readonly("gfx", &Media::gfx)
        .def_readonly("fonts", &Media::fonts)
        ;

    // Expose Process object
    class_<Process, ProcessWrapper, boost::noncopyable, boost::shared_ptr<ProcessWrapper> >("Process", init<>())
        .def("Execute", &Process::Execute, &ProcessWrapper::Execute_default)
        .def("Init", &Process::Init, &ProcessWrapper::Init_default)

        .add_property("x", make_getter(&Process::x), make_setter(&Process::x))
        .add_property("y", make_getter(&Process::y), make_setter(&Process::y))
        .add_property("z", make_getter(&Process::z), make_setter(&Process::z))

        .add_property(
            "image",
            make_getter(&Process::image, return_value_policy<reference_existing_object>()),
            make_setter(&Process::image)
            )

        .def("move_forward", &Process::move_forward)
        .def("Kill", &Process::Kill)
        ;

    // Expose Text object
    class_<Text, TextWrapper, boost::noncopyable, boost::shared_ptr<TextWrapper> >("Text", init<Font*, float, float, int, string>())
        .add_property(
            "text",
            make_getter(&Text::text),
            &Text::set_text
            )
        ;

    // Expose the main app obj
    class_<Main_App>("Main_App")
        .add_property("current_fps", make_getter(&Main_App::current_fps))
        .add_property("process_count", make_getter(&Main_App::process_count))
        .add_property("media", make_getter(&Main_App::media, return_value_policy<reference_existing_object>()))
        .def("Keyboard_key_down", &Main_App::Keyboard_key_down)
        .def("Quit", &Main_App::Quit)
        ;

    // Expose the framework constants
    scope().attr("TEXT_ALIGN_TOP_LEFT") = TEXT_ALIGN_TOP_LEFT;
/*
#define TEXT_ALIGN_TOP_LEFT 0
#define TEXT_ALIGN_TOP 1
#define TEXT_ALIGN_TOP_RIGHT 2
#define TEXT_ALIGN_CENTER_LEFT 3
#define TEXT_ALIGN_CENTER 4
#define TEXT_ALIGN_CENTER_RIGHT 5
#define TEXT_ALIGN_BOTTOM_LEFT 6
#define TEXT_ALIGN_BOTTOM 7
#define TEXT_ALIGN_BOTTOM_RIGHT 8 
*/


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

        object main_module = import("__main__");
        object main_namespace = main_module.attr("__dict__");

        initgame_core();

        // Give the main app instance
        main_namespace["game"] = ptr(game);

        object ignored = exec_file(
            "core/main.py",
            main_namespace
            );

    }
    catch(error_already_set const &)
    {

        PyErr_Print();
        return False;

    }

    return True;

}

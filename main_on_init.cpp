/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Main app initialisation
 ****************************/

#include <iostream>
using namespace std;
#include "main.h"



using namespace boost::python;


BOOST_PYTHON_MODULE(game_core)
{
    
    // Expose all media related objects
    class_< boost::shared_ptr<Image> >("Image");
    class_< boost::shared_ptr<Font> >("Font");
    class_<gfx_map> ("gfxMap")
        .def(map_indexing_suite<gfx_map>())
    ;
    class_<Media>("Media")
        .def_readonly("gfx", &Media::gfx)
        ;

    // Expose Process object
    class_<Process, ProcessWrapper, boost::noncopyable, boost::shared_ptr<ProcessWrapper> >("Process", init<>())
        .def("Execute", &Process::Execute, &ProcessWrapper::Execute_default)
        .add_property(
            "image",
            make_getter(&Process::image, return_internal_reference<1, with_custodian_and_ward<1, 2> >()),
            make_setter(&Process::image)
            )
        ;

    // Expose the main app obj
    class_<Main_App>("Main_App")
        .add_property("current_fps", &Main_App::python_property_get_current_fps)
        .add_property("media", make_getter(&Main_App::media, return_value_policy<reference_existing_object>()))
        ;

}

 
bool Main_App::On_Init()
{

    // Initialise SDL
    if(SDL_Init(SDL_INIT_EVERYTHING) < 0)
        return False;
    if(TTF_Init() < 0)
        return False;

    // create window
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 2);
    surf_display = SDL_SetVideoMode(640, 480, 32, SDL_HWSURFACE | SDL_GL_DOUBLEBUFFER | SDL_OPENGL);

    if(surf_display == NULL)
        return False;

    // set up opengl context
    glClearColor(0, 0, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT);

    glViewport(0, 0, 640, 480);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glOrtho(0, 640, 480, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);

    glEnable(GL_TEXTURE_2D);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_LINE_SMOOTH);

    // Need this little titbit
    default_texture_coords[0] = 1.0f;
    default_texture_coords[1] = 1.0f;
    default_texture_coords[3] = 1.0f;
    default_texture_coords[4] = 1.0f;

    // Start up python
    try
    {

        object main_module = import("__main__");
        object main_namespace = main_module.attr("__dict__");

        initgame_core();

        // Give the main app instance
        main_namespace["game"] = ptr(this);

        object ignored = exec_file(
            "core/main.py",
            main_namespace
            );

    }
    catch(error_already_set const &)
    {
        PyErr_Print();
    }

    // Init game
    media = new Media();
    //new Main_input(this);

    return True;

}


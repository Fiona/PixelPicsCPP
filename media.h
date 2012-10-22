/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Media object header
 ****************************/

#ifndef _MEDIA_H_
#define _MEDIA_H_
 
#include <string>
#include <map>
using namespace std;


typedef std::map <string, Image* > gfx_map;
typedef std::map <string, Font* > font_map;
typedef std::map <string, SFX* > sfx_map;
typedef std::map <string, Music* > music_map;


/*
 */ 
class Media
{

public:
    Media();
    Media(Main_App* _game);
    ~Media();

    Main_App* game;
    gfx_map gfx;
    font_map fonts;
    sfx_map sfx;
    music_map music;

};

 
#endif

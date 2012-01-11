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


/*
 */ 
class Media
{

public:
    Media();
    ~Media();

    gfx_map gfx;
    font_map fonts;

};

 
#endif

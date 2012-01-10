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


typedef std::map <string, boost::shared_ptr<Image> > gfx_map;


/*
 */ 
class Media
{

public:
    Media();
    ~Media();

    gfx_map gfx;
    map<string,Font*> fonts;

};
 
#endif

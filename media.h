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

/*
 */ 
class Media
{

public:
    Media();
    ~Media();

    map<string,Image*> gfx;
    map<string,Font*> fonts;

};
 
#endif

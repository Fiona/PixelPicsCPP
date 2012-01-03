/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Font loading
 ****************************/

#ifndef _FONT_H_
#define _FONT_H_
 
#include <string>
using namespace std;

/*
 */ 
class Font
{

public:
    TTF_Font* font;
    
    Font();
    Font(string _filename, int _size);
    ~Font();

    string filename;
    int size;

};
 
#endif

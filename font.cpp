/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Font loading
 ****************************/

#include "main.h"
using namespace std;


Font::Font(){ }

Font::Font(string _filename, int _size)
{

    filename = _filename;
    size = _size;

    font = TTF_OpenFont(filename.c_str(), size);
 
    if(font == NULL)
        return;

}


Font::~Font()
{

    if(font != NULL)
    {
        TTF_CloseFont(font);
        font = NULL;
    }

}

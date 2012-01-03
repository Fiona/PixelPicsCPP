/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Media object source file
 ****************************/


#include <string>
using namespace std;

#include "main.h"


Media::Media()
{

    gfx.insert(pair<string,Image*>("ship", new Image("ship.png")));
    gfx.insert(pair<string,Image*>("shot", new Image("shot.png")));

}


Media::~Media()
{

    for(map<string, Image*>::iterator it = gfx.begin(); it != gfx.end(); ++it)
    {
        if(it->second == NULL)
            continue;
        delete it->second;
    }

}

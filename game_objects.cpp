/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Game objects
 ****************************/


#include "game_objects.h"

#include <iostream>


Main_input::Main_input(Main_App* _game): Process()
{

    game = _game;
    current_rotation = 0;
    current_rotation_2 = 0;

    current_fps_display = new Text(game->media->fonts["basic"], .0f, .0f, TEXT_ALIGN_TOP_LEFT, "");
    current_process_count_display = new Text(game->media->fonts["basic"], .0f, 20.0f, TEXT_ALIGN_TOP_LEFT, "");
    new Ship(game, 300.0f, 200.0f);

}


void Main_input::Execute()
{

    if(game -> Keyboard_key_down(SDLK_ESCAPE))
        game -> Quit();

    create_vorticies(200.0f, 300.0f, 1);
    create_vorticies(400.0f, 300.0f, 1);

    current_fps_display->set_text(str(boost::format("FPS: %1%") % game->current_fps));
    current_process_count_display->set_text(str(boost::format("Num processes: %1%") % Process::Process_List.size()));

}


void Main_input::create_vorticies(float x, float y, int type)
{
    int range = 0;
    int amount = 3;

    if(game->Keyboard_key_down(SDLK_SPACE))
    {
        range = 150;
        amount = 10;
    }

    for(int c = 0; c <= range; c++)
    {
        if(type == 1)
            current_rotation_2 -= amount;
        else
            current_rotation += amount;

        if(type == 1)
        {
            if(current_rotation_2 < -360)
                current_rotation_2 = 0;
        }
        else
        {
            if(current_rotation > 360)
                current_rotation = 0;
        }

        new Shot(game, x, y, (type == 1 ? current_rotation_2 : current_rotation));        
    }
}


// ----------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------


Ship::Ship(Main_App* _game, float pos_x, float pos_y): Process()
{
    x = pos_x;
    y = pos_y;
    z = -100;
    game = _game;
    image = game->media->gfx["ship"];
}


void Ship::Execute()
{
    if(game->Keyboard_key_down(SDLK_LEFT))
        x -= 10.0;
    if(game->Keyboard_key_down(SDLK_RIGHT))
        x += 10.0;
    if(game->Keyboard_key_down(SDLK_UP))
        y -= 10.0;
    if(game->Keyboard_key_down(SDLK_DOWN))
        y += 10.0;
}


// ----------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------


Shot::Shot(Main_App* _game, float pos_x, float pos_y, int _rotation_to): Process()
{
    x = pos_x;
    y = pos_y;
    z = 100;
    game = _game;
    rotation_to = _rotation_to;
    image = game->media->gfx["shot"];
}


void Shot::Execute()
{
    //move_forward(3.0, rotation_to);

    if(x < 50.0f || x > 590.0f || y < 0.0f || y > 480.0f)
        Kill();
}

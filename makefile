EXECUTABLE=pixelpics
SOURCES=main.cpp \
main_on_init.cpp \
main_on_cleanup.cpp \
main_on_event.cpp \
main_on_loop.cpp \
main_on_render.cpp \
image.cpp \
process.cpp \
game_objects.cpp \
media.cpp

CC=g++
CFLAGS=-c -Wall
SDLFLAGS=-static -lSDL `sdl-config --static-libs` -lSDL_image
OBJECTS=$(SOURCES:.cpp=.o)

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(OBJECTS) -o $@ $(SDLFLAGS) 

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm *.o 

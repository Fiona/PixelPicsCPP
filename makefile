EXECUTABLE=pixelpics
SOURCES=main.cpp \
main_on_init.cpp \
main_on_cleanup.cpp \
main_on_event.cpp \
main_on_loop.cpp \
main_on_render.cpp \
image.cpp \
font.cpp \
process.cpp \
game_objects.cpp \
media.cpp


CC=g++
CFLAGS=-c -Wall

#SDLFLAGS=-Wl,-Bstatic `sdl-config --static-libs` -lSDL_image -lSDL_ttf -lfreetype -lz -Wl,-Bdynamic -lGL
SDLFLAGS= -lGL -lGLU `sdl-config --libs` -lSDL_image -lSDL_ttf -lfreetype -lz
OBJECTS=$(SOURCES:.cpp=.o)

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(OBJECTS) $(SDLFLAGS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm *.o 

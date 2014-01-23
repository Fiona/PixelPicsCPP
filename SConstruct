# Setup
import os
env = Environment()

# Tools
def walk_subdirs(path_dir) :  
    list = [name for name in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, name)) and name[0] != '.']
    list.sort()
    return list

# Libraries
env.Append(CPPPATH = ['/usr/include/python2.7/'])
env.Append(LIBS = ['SDL', 'pthread', 'm', 'dl', 'SDL_image', 'SDL_ttf', 'SDL_mixer', 'freetype', 'z', 'bz2', 'GL', 'GLU', 'python2.7', 'boost_python', 'boost_filesystem', 'boost_system'])

# List of sources
sources = Glob('*.cpp')

# Switch to debug
debug = ARGUMENTS.get('debug', 0)
if int(debug):
   env.Append(CCFLAGS = '-g')
else:
   env.Append(CCFLAGS = '-O')

# Build executable
object_list = env.Object(source = sources)
main_executable = env.Program(target = 'pixelpics', source = object_list)

Default(main_executable)


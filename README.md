# intphys-2.0

#### Data generation for the Intuitive Physics Challenge - http://www.intphys.com

Developed with
[Unreal Engine](https://www.unrealengine.com/what-is-unreal-engine-4)
4.18 and the [UnrealEnginePython](https://github.com/20tab/UnrealEnginePython)
plugin.

The 2.0 version of intphys is a reimplementation of intphys-1.0 based on UE-4.18 (was
UE-4.8) using the Python scripting language (was Lua).


## Video exemples

#### Train samples

Train samples are always physically possible and have high variability

<img src="Exemples/gif/train_1.gif" width="150"> <img src="Exemples/gif/train_2.gif" width="150"> <img src="Exemples/gif/train_3.gif" width="150"> <img src="Exemples/gif/train_4.gif" width="150">


#### Test samples

Test samples have a constrained variability and come as quadruplets: 2
possibles cases and 2 impossibles ones

<img src="Exemples/gif/test_1.gif" width="150"> <img src="Exemples/gif/test_2.gif" width="150"> <img src="Exemples/gif/test_3.gif" width="150"> <img src="Exemples/gif/test_4.gif" width="150">


#### Metadata

Each video comes with it's associated depth field and object masking
(each object have a unique id), along with a detailed status in JSON
format.

<img src="Exemples/gif/meta_1.gif" width="150"> <img src="Exemples/gif/meta_2.gif" width="150"> <img src="Exemples/gif/meta_3.gif" width="150">


## Installation details

This installation process succeeded on Debian stable (Jessie) and
Ubuntu 16.04. It may be fine for other Unices as well, but this have
not been tested.

* First of all setup an Epic Games account at
  https://github.com/EpicGames/Signup/, needed to clone the Unreal
  Engine repository from github.

* Install Unreal Engine as documented
  [here](https://github.com/EpicGames/UnrealEngine/blob/release/Engine/Build/BatchFiles/Linux/README.md).
  Basically have a:

        git clone https://github.com/EpicGames/UnrealEngine -b release
        cd UnrealEngine
        ./Setup.sh
        ./GenerateProjectFiles.sh
        make

* Install intphys in a separate directory. Clone the repository and
  its UnrealEnginePython submodule from github. Do not forget the
  `--recursive` option to download the submodule:

        git clone --recursive git@github.com:bootphon/intphys.git

* You need Python>=3.6 installed as `/usr/bin/python3.6` (else you
  need to tweak the UnrealEnginePython plugin
  [here](https://github.com/20tab/UnrealEnginePython/blob/master/Source/UnrealEnginePython/UnrealEnginePython.Build.cs#L11)
  so that it can find python>=3.6 in a non-standard path, for exemple
  in a virtual environment). You also need the dataclasses module (in
  the standard library with python>=3.7). To install it on ubuntu
  16.04, have a:

        sudo add-apt-repository ppa:jonathonf/python-3.6
        sudo apt-get update
        sudo apt-get install python3.6 python3.6-dev
        /usr/bin/python3.6 -m pip install dataclasses

* The intphys code reads the path to UnrealEngine and the path to the
  Python scripts from the `UE_ROOT` and `PYTHONPATH` environment
  variables repectively. Add that to your `~/.bashrc`:

        export UE_ROOT=/absolute/path/to/UnrealEngine
		export PYTHONPATH=$PYTHONPATH:/absolute/path/to/intphys/Content/Scripts

* We now need to package the intphys project into a standalone binary
  program. Just have a:

        ./Tools/build_package.sh


## Usage

* Use the `intphys.py` program to run the game and generate data. To
  discover the arguments, have a:

        ./intphys.py --help

* The basic usage is calling `intphys.py scenes.json -o
  ./output_data`. This reads the scenes to be generated from the
  `scenes.json` file and write them in the folder `./output_data`.

* Generate scenes using the packaged game:

        ./intphys.py Examples/example.json

* When developing you may want to run the project within UE4Editor
  (`--editor` option) or as a standalone game (`--standalone-game`
  option). The `--verbose` option is usefull for dev as well.


## Additional utils

In the `Tools` directory are stored few utility scripts:

* **images2video.sh** : converts a sequence of images into a video or
  a gif file. Used to postprocess the generated png images.

* **clean.sh** : deletes the intphys build/binaries directories.

* **make_archives.py** : build tar.gz archives as released on
  www.intphys.com.

* scripts for building the project.

In the `Exemples` directory are stored scripts to generate few videos,
extract them to gif pictures and embeed them in a html page.


## Tweaks

Here are some tweaks and error reports usefull for intphys
development.


### UE4 crash: cannot open OpenGL context

Occured after an update of the nvidia graphic drivers. Just reboot and
try again. `sudo glxinfo` helps.


### Precompiled headers

After a system update you may issue an error when running
`./Tools/build_package.sh` about `.gch` precompiled headers. The issue is like:

    fatal error: file '/usr/include/linux/version.h' has been modified since the precompiled header '.../UE4Editor/Development/Engine/SharedPCH.Engine.h.gch' was built
    note: please rebuild precompiled header '.../UE4Editor/Development/Engine/SharedPCH.Engine.h.gch'

In that case remove all the `.gch` files and recompile the engine:

    cd $UE_ROOT
    find Engine/Intermediate -type file -name *.gch -delete
    ./GenerateProjectFiles.sh && make

### How to make a new project

Steps to duplicate the intphys project into a fresh one in
UnrealEngine. This may be needed for debug or development or when
upgrading to a new engine version.

1. Open UE4Editor and create a new C++ blank project called `intphys`
   in the `new` directory, open the project a first time and
   close it just after.

2. Copy the following files and folders from `old` to `new`:

    - Config
    - Content
    - Source/intphys
    - Plugins
    - DeprecatedLua
    - Exemples
    - Tools
    - .git
    - and all the top-level files in the git repo (.gitignore,
      configure, etc...)

3. Reopen the project. In Project Settings / Maps & Mods, set up the
   default map to intphysMap.

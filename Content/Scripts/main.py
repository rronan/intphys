import importlib
import json
import os
import random
import sys
import math

import unreal_engine as ue
from unreal_engine.classes import KismetSystemLibrary, GameplayStatics
from unreal_engine import FVector, FRotator

from object import Object
from camera import Camera
from floor import Floor
from wall import Wall

# the default screen resolution (in pixels)
width, height = 288, 288

class Main:    
    def init_random_seed(self):
        # init random number generator with a seed
        try:
            seed = os.environ['INTPHYS_SEED']
        except KeyError:
            seed = None

        ue.log('init random numbers generator{}'.format(
            '' if seed is None else ', seed is {}'.format(seed)))

        random.seed(seed)

    def init_resolution(self):
        try:
            resolution = os.environ['INTPHYS_RESOLUTION']
        except KeyError:
            resolution = str(width) + 'x' + str(height)
            ue.log('INTPHYS_RESOLUTION not defined, using default')

        ue.log('set screen resolution to {}'.format(resolution))
        KismetSystemLibrary.ExecuteConsoleCommand(
            self.uobject.get_world(),
            'r.SetRes {}'.format(resolution))

    def init_configuration(self):
        try:
            json_file = os.environ['INTPHYS_CONFIG']
        except KeyError:
            self.exit_ue(
                'fatal error, INTPHYS_CONFIG not defined, exiting')
        ue.log('loading configuration from {}'.format(json_file))

        try:
            output_dir = os.environ['INTPHYS_DATADIR']
        except KeyError:
            self.exit_ue(
                'fatal error, INTPHYS_DATADIR not defined, exiting')
        ue.log('writing data to {}'.format(output_dir))

        config = configuration.Configuration(json_file, output_dir)

        ue.log('generation of {nscenes} scenes ({ntest} for test and '
               '{ntrain} for train), total of {niterations} iterations'.format(
            nscenes=config.nruns_test + config.nruns_train,
            ntest=config.nruns_test,
            ntrain=config.nruns_train,
            niterations=len(config.iterations)))

    # def load_scenes(self):
    #     try:
    #         scenes_file = os.environ['INTPHYS_SCENES']
    #     except KeyError:
    #         self.exit_ue('fatal error, INTPHYS_SCENES not defined, exiting')
    #         return
    #     scene_raw = json.loads(open(scenes_file, 'r').read())

    def exit_ue(self, message=None):
        """Quit the game, optionally displaying an error message"""
        if message:
            ue.log_error(message)
        KismetSystemLibrary.QuitGame(self.world)

    def begin_play(self):
        self.world = self.uobject.get_world()
        ue.log('Raising up new world {}'.format(self.world.get_name()))

        # init the seed for random parameters generation
        self.init_random_seed()

        # init the rendering resolution
        self.init_resolution()

        # spawn the camera and attach the viewport to it
        camera = Camera(self.world, FVector(0, 0, 2000), FRotator(-90, 0, 0))

        # spawn an actor
        floor = Floor(self.world, "/Game/Materials/Floor/M_Ground_Gravel")
        object = Object(self.world, Object.shape['Sphere'], FVector(0, 0, 0), FRotator(0, 0, 0), "/Game/Materials/Object/BlackMaterial")
        object2 = Object(self.world, Object.shape['Sphere'], FVector(0, 0, 0), FRotator(0, 0, 0), "/Game/Materials/Object/GreenMaterial")
        #wall = Wall(self.world, "/Game/Materials/Object/BlackMaterial")

"""Block O3 is spatio-temporal continuity, spheres only"""
import random
from scenario.mirrorTest import MirrorTest
from scenario.train import Train
from unreal_engine import FVector
from unreal_engine.classes import ScreenshotManager
import unreal_engine as ue


class O3Base:
    @property
    def name(self):
        return 'O3'

    @property
    def description(self):
        return 'bloc O3'


class O3Train(O3Base, Train):
    pass


class O3Test(O3Base, MirrorTest):
    def __init__(self, world, saver, is_occluded, movement):
        super().__init__(world, saver, is_occluded, movement)
        self.check_array[0]['visibility'] = []
        self.check_array[0]['location'] = []
        self.check_array[1]['visibility'] = []
        self.check_array[1]['location'] = []

    def setup_magic_actor(self):
        if self.run == 1:
            magic_actor = self.actors[self.params['magic']['actor']]
            current_location = magic_actor.actor.get_actor_location()
            target_location = FVector(0, 0, 0)
            if 'static' in self.movement:
                target_location = FVector(current_location.x +
                                          random.randint(-500, 500),
                                          current_location.y + 
                                          random.randint(-500, 500),
                                          current_location.z)
            elif '1' in self.movement:
                target_location = FVector(current_location.x,
                                          current_location.y +
                                          random.randint(50, 75) if magic_actor.actor.get_actor_location().y < 0 else random.randint(-75, 50),
                                          current_location.z)
            else:
                target_location = FVector(current_location.x,
                                          current_location.y +
                                          100,
                                          current_location.z)
            magic_actor.set_location(target_location)

    # this function is here so you can put only the attribute that please you
    # in the check array. It is called every tick
    # there is two dictionaries : one for each run
    def fill_check_array(self):
        magic_actor = self.actors[self.params['magic']['actor']].actor
        self.check_array[self.run]['location'].append(
            magic_actor.get_actor_location())
        ignored_actors = []
        for actor_name, actor in self.actors.items():
            if 'object' not in actor_name.lower() and \
                    'occluder' not in actor_name.lower():
                if 'walls' in actor_name.lower():
                    ignored_actors.append(actor.front.actor)
                    ignored_actors.append(actor.left.actor)
                    ignored_actors.append(actor.right.actor)
                else:
                    ignored_actors.append(actor.actor)
        visible = ScreenshotManager.IsActorInLastFrame(
            magic_actor, ignored_actors)[0]
        self.check_array[self.run]['visibility'].append(visible)

    def static_visible(self):
        visibility_array = self.checks_time_laps("visibility", True)
        # if the number of frame where the magic actor is visible is less than
        # 4 time the number of magic tick required, scene need to be restarted
        if len(visibility_array) < 4:
            return False
        self.params['magic']['tick'] = random.choice(visibility_array)
        return True

    def dynamic_1_visible(self):
        visibility_array = self.checks_time_laps('visibility', True)
        # if the number of frame where the magic actor is visible is less than
        # 4 time the number of magic tick required, scene need to be restarted
        if len(visibility_array) < 4:
            return False
        self.params['magic']['tick'] = random.choice(visibility_array)
        # TODO length of the jump
        return True

    def dynamic_2_visible(self):
        visibility_array = self.checks_time_laps('visibility', True)
        # if the number of frame where the magic actor is visible is less than
        # 4 time the number of magic tick required, scene need to be restarted
        if len(visibility_array) < 8:
            return False
        self.params['magic']['tick'] = []
        self.params['magic']['tick'].append(random.choice(visibility_array))
        visibility_array.remove(self.params['magic']['tick'][0])
        self.params['magic']['tick'].append(random.choice(visibility_array))
        self.params['magic']['tick'].sort()
        return True

    def static_occluded(self):
        visibility_array = self.checks_time_laps('visibility', False)
        # if the number of frame where the magic actor is visible is less than
        # 4 time the number of magic tick required, scene need to be restarted
        if len(visibility_array) < 4:
            return False
        self.params['magic']['tick'] = random.choice(visibility_array)
        return True

    def dynamic_1_occluded(self):
        visibility_array = self.checks_time_laps('visibility', False)
        temp_array = visibility_array
        # remove the last occurences of not visible actor if
        # it is out of the fieldview
        if visibility_array[-1] == 199:
            previous_frame = 0
            for frame in reversed(temp_array):
                if frame == 199 or frame + 1 == previous_frame:
                    previous_frame = frame
                    visibility_array.remove(frame)
        temp_array = visibility_array
        occlusion = []
        occlusion.append([])
        i = 0
        previous_frame = temp_array[0] - 1
        # distinguish the different occlusion time laps
        for frame in temp_array:
            if frame - 1 != previous_frame:
                i += 1
                occlusion.append([])
            occlusion[i].append(frame)
            previous_frame = frame
        # if there is less than 2 distinct occlusion the scene will restart
        self.params['magic']['tick'] = random.choice(occlusion[0])
        return True

    def dynamic_2_occluded(self):
        visibility_array = self.checks_time_laps('visibility', False)
        temp_array = visibility_array
        # remove the last occurences of not visible actor if
        # it is out of the fieldview
        if visibility_array[-1] == 199:
            previous_frame = 0
            for frame in reversed(temp_array):
                if frame == 199 or frame + 1 == previous_frame:
                    previous_frame = frame
                    visibility_array.remove(frame)
        temp_array = visibility_array
        occlusion = []
        occlusion.append([])
        i = 0
        previous_frame = temp_array[0] - 1
        # distinguish the different occlusion time laps
        for frame in temp_array:
            if frame - 1 != previous_frame:
                i += 1
                occlusion.append([])
            occlusion[i].append(frame)
            previous_frame = frame
        # if there is less than 2 distinct occlusion the scene will restart
        if len(occlusion) < 2:
            return False
        self.params['magic']['tick'] = []
        self.params['magic']['tick'].append(random.choice(occlusion[0]))
        self.params['magic']['tick'].append(random.choice(occlusion[1]))
        return True

    def set_magic_trick(self):
        if super().set_magic_trick() is False:
            return False
        if isinstance(self.params['magic']['tick'], int):
            magic_tick = self.params['magic']['tick']
            if self.check_array[0]['location'][magic_tick] == \
                    self.check_array[1]['location'][magic_tick]:
                ue.log_warning("Magic actor location doesn't match in \
                               each possible run")
                return False
        else:
            magic_tick = self.params['magic']['tick']
            if self.check_array[0]['location'][magic_tick][0] == \
                    self.check_array[1]['location'][magic_tick][0] or \
                    self.check_array[0]['location'][magic_tick][1] == \
                    self.check_array[1]['location'][magic_tick][1]:
                ue.log_warning("Magic actor location doesn't match in \
                               each possible run")
                return False

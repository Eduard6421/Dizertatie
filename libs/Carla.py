import carla
import random

class Carla():

    def __init__(self, host, ip):
        self.client = carla.Client(host,ip)
        self.world = self.client.get_world()

    def load_world(self, world_name):
        self.client.load_world('/Game/Carla/Maps/Town02')
        self.world = self.get_world()

    def get_available_worlds(self):
        return self.client.get_available_maps()
    
    def wait_for_tick(self):
        self.world.wait_for_tick()

    def get_snapshot(self):
        return self.world.get_snapshot()

    def get_world(self):
        return self.client.get_world()
    
    def get_map(self):
        return self.world.get_map()

    def get_random_location_from_navigation(self):
        return self.world.get_random_location_from_navigation()

    def getBaseTransform(self):
        return carla.Transform()

    def get_actor(self, actor_id):
        return self.world.get_actor(actor_id)

    def get_actors(self,ids):
        return self.world.get_actors(ids)

    def get_random_walker_blueprint(self):
        return random.choice(self.world.get_blueprint_library().filter('walker.pedestrian.*'))

    def get_random_vehicle_blueprint(self):
        return random.choice(self.world.get_blueprint_library().filter('vehicle.*'))
    
    def get_walker_controller_blueprint(self):
        return self.world.get_blueprint_library().find('controller.ai.walker')

    def get_all_walker_blueprints(self):
        return self.world.get_blueprint_library().filter('walker.*')
    
    def get_all_vehicle_blueprint(self):
        return self.world.get_blueprint_library().filter('vehicle.*')

    def get_random_spawn_point(self):
        return random.choice(self.world.get_map().get_spawn_points())

    def get_spawn_points(self):
        return self.world.get_map().get_spawn_points()

    def command_spawn_actor(self, blueprint, spawn_point, parent = None):
        if parent is None:
            return carla.command.SpawnActor(blueprint, spawn_point)
        else:
            return carla.command.SpawnActor(blueprint, spawn_point, parent)
        
    def command_delete_actor(self, actor):
        return carla.command.DestroyActor(actor)

    def apply_command_sync(self, command):
        return self.client.apply_batch_sync([command], True)[0]

    def apply_commands_sync(self, commands):
        return self.client.apply_batch_sync(commands, True)

    def try_spawn_actor(self, blueprint, spawn_point):
        self.world.try_spawn_actor(blueprint, spawn_point)

    def set_weather(self, weather_config):
        self.world.set_weather(weather_config)
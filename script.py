
import time
import carla

from libs.Carla import Carla
from libs.WeatherBuilder import WeatherBuilder
from libs.SettingsBuilder import SettingsBuilder
from libs.Controller import buildPipeline, simulateStep, spawnWalkers
from libs.Spawner import DespawnPedestrians


carla_client = Carla('localhost', 2000)


def __main__():

    carla_settings  = SettingsBuilder.get_world_config()
    carla_client.set_world_settings(carla_settings)

    #weather_config= WeatherBuilder.get_weather_config()
    #carla_client.set_weather(weather_config)

    walkers = None
    num_agents = 100
    step = 10

    try:

        walkers = spawnWalkers(carla_client,num_agents)
        action_pipeline = buildPipeline()

        while True:
            simulateStep(carla_client,action_pipeline,step)
            print('ran tick')

    except KeyboardInterrupt:
        pass
    finally:
        DespawnPedestrians(carla_client,walkers)
        print('Despawned')


if __name__ == "__main__":
    __main__()